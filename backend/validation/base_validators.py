import regex as re
from datetime import datetime
from werkzeug.exceptions import BadRequest
from urllib.parse import urlparse

# --------------------------------------
# Constants (Group all titles and regex)
# --------------------------------------

# ----- Title Part ----
TITLES = {

    "mr", "mr.", "mrs", "mrs.", "ms", "ms.", "miss",
    "dr", "dr.", "prof", "prof.", "sir", "madam", "coach"
}
TITLES_WITH_DOT = {"mr", "mrs", "ms", "dr", "prof"}
# ----- Will Remove later after frontend implementation ----

NAME_ALLOWED_REGEX = r"^[\p{L}’'\- ]+$"
PHONE_REGEX = r"^\+?[0-9 ]{7,20}$"
CHAT_REGEX = r"^(?=.*[A-Za-z0-9])[A-Za-z0-9 @+_.\-():]{3,50}$"
EXPERTISE_REGEX = r"^(?=.*[A-Za-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ0-9 ,/&+\-()]{2,100}$"
EMAIL_REGEX = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,100}$"

# -------------------------------------
# Normalization and whitespace helpers
# -------------------------------------

def strip_whitespace(value: str) -> str:
    if not isinstance(value, str):
        raise BadRequest({"error": "Value must be a string", "value": value})
    # Normalize apostrophes to ASCII '
    value = value.replace("’", "'").replace("ʻ", "'").replace("ʹ", "'")
    # Remove tabs/newlines
    value = value.replace("\t", " ").replace("\n", " ")
    # Collapse multiple spaces → single space
    value = re.sub(r"\s+", " ", value)

    return value.strip()

# --------------------------------------------
# Generic validators (string, int, bool, date)
# --------------------------------------------

def require_fields(data, required):
    missing = [f for f in required if f not in data]
    if missing:
        raise BadRequest({
            "error": "Missing required fields",
            "fields": missing
        })

def validate_string(field, value, min_len=1, max_len=255): # generic validator
    if not isinstance(value, str):
        raise BadRequest({
            "error": f"{field} must be a string",
            "value": value
        })
    if not (min_len <= len(value) <= max_len):
        raise BadRequest({
            "error": f"{field} length must be between {min_len} and {max_len}",
            "actual_length": len(value)
        })

def validate_int(field, value, min_val=None, max_val=None):
    if not isinstance(value, int):
        raise BadRequest({
            "error": f"{field} must be an integer",
            "value": value
        })
    if min_val is not None and value < min_val:
        raise BadRequest({
            "error": f"{field} must be >= {min_val}",
            "value": value
        })
    if max_val is not None and value > max_val:
        raise BadRequest({
            "error": f"{field} must be <= {max_val}",
            "value": value
        })

# Validate boolean type
def validate_bool(field, value):
    if not isinstance(value, bool):
        raise BadRequest({
            "error": f"{field} must be true or false",
            "value": value
        })

# Validate YYYY-MM-DD date format
def validate_date(field, value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except Exception:
        raise BadRequest({
            "error": f"{field} must be a valid date in YYYY-MM-DD format",
            "value": value
        })

# ----------------------------------------------------
# Custom validators (unicode name, startup name, role)
# ----------------------------------------------------

def validate_person_name(field: str, value: str, min_len: int, max_len: int) -> str:
    value = strip_whitespace(value)
    validate_string(field, value, min_len, max_len)
    pattern = r"^[\p{L}\p{M}\p{Zs}'\-]+$"

    import regex as reg
    if not reg.match(pattern, value):
        raise BadRequest({
            "error": f"{field} contains invalid characters",
            "allowed": "Unicode letters, accents, hyphens, apostrophes, spaces",
            "value": value
        })

    return value

def validate_startup_name(field, value, min_len=1, max_len=100):
    value = strip_whitespace(value)
    validate_string(field, value, min_len, max_len)

    pattern = r"^[\p{L}\p{N}\p{M}\p{Zs}._+\-'&,/() \u200d\ufe0f\p{So}]+$"

    try:
        import regex as reg
        if not reg.match(pattern, value):
            raise BadRequest({
                "error": f"{field} contains invalid characters",
                "allowed": "Unicode letters, numbers, spaces, hyphens, underscores, dots, plus signs, apostrophes, ampersands, slashes, commas, parentheses",
                "value": value
            })
    except ImportError:
        # Fallback: basic check
        for ch in value:
            if ch.isalnum() or ch in " ._+-":
                continue
            raise BadRequest({
                "error": f"{field} contains invalid characters",
                "value": value
            })

    return value

def validate_startup_description(value: str) -> str:
    value = value.strip()

    # Block HTML/script tags
    if "<" in value or ">" in value:
        raise BadRequest({"error": "StartupDescription must not contain HTML or script tags"})
    # Length limit
    if len(value) > 255:
        raise BadRequest({"error": "StartupDescription is too long"})
    return value

def validate_role(field, value, min_len=2, max_len=50):
    value = strip_whitespace(value)
    validate_string(field, value, min_len, max_len)

    pattern = r"^[\p{L}\p{M}0-9.\-` ']+$"

    try:
        import regex as reg
        if not reg.match(pattern, value):
            raise BadRequest({
                "error": f"{field} contains invalid characters",
                "allowed": "letters, numbers, spaces, hyphens",
                "value": value
            })
    except ImportError:
        for ch in value:
            if ch.isalnum() or ch in "- ":
                continue
            raise BadRequest({
                "error": f"{field} contains invalid characters",
                "value": value
            })

    return value

# Flexible social media validator (used by coaches + startups)
def validate_social_media_flexible(sm: dict):
    warnings = []

    if sm is None:
        return None, warnings

    if not isinstance(sm, dict):
        raise BadRequest({"error": "SocialMedia must be an object"})

    cleaned = {}

    for key, value in sm.items():
        v = strip_whitespace(value)

        # Block unsafe schemes
        if v.lower().startswith(("javascript:", "data:", "file:")):
            raise BadRequest({"error": f"SocialMedia.{key} contains an unsafe URL"})

        # Block script injection
        if "<script>" in v.lower() or "</script>" in v.lower():
            raise BadRequest({"error": f"SocialMedia.{key} contains script injection"})

        # Full URL → validate structure
        if v.startswith(("http://", "https://")):
            parsed = urlparse(v)
            if not parsed.netloc:
                raise BadRequest({"error": f"SocialMedia.{key} must contain a valid domain"})
            cleaned[key] = v
            continue

        # Handle -> accept as plain text
        if v.startswith("@"):
            warnings.append(f"{key}: handle accepted as plain text")
            cleaned[key] = v
            continue

        # Domain-like -> normalize
        if "." in v:
            normalized = "https://" + v
            warnings.append(f"{key}: normalized to URL")
            cleaned[key] = normalized
            continue

        # Otherwise accept as plain text
        cleaned[key] = v

    return cleaned, warnings

def validate_free_text(field, value):
    if not isinstance(value, str):
        raise BadRequest({
            "error": f"{field} must be a string",
            "value": value
        })

    # Normalize apostrophes
    value = value.replace("’", "'").replace("ʻ", "'").replace("ʹ", "'")
    # Normalize whitespace
    value = value.replace("\t", " ").replace("\n", " ")
    value = re.sub(r"\s+", " ", value).strip()

    return value

# ------------------------------------------------------------------
# Name processing helpers (normalize, insert spaces, remove symbols)
# ------------------------------------------------------------------

def normalize_name(text):
    if not text:
        return ""
    text = text.replace("’", "'")
    text = " ".join(text.split())
    return text.strip()

# Alphanumeric-only validator
def validate_no_symbols(field, value):
    value = strip_whitespace(value)

    # Remove spaces before checking
    if not value.replace(" ", "").isalnum():
        raise BadRequest({
            "error": f"{field} must contain only letters and numbers",
            "value": value
        })
    return value

def validate_name_characters(field_name, value):
    if not re.match(NAME_ALLOWED_REGEX, value):
        raise BadRequest({ "error": f"{field_name} contains invalid characters" })

def validate_email(field_name, value):
    if not value:
        raise ValueError(f"{field_name} is required")
    value = value.strip()
    if not re.match(EMAIL_REGEX, value):
        raise ValueError(f"{field_name} must be a valid email address")

    return value

# ---------------------------------------------------------------------
# Coach-specific validators (phone, chat, bio, expertise, social media)
# ---------------------------------------------------------------------

def validate_coach_phone(value: str) -> str:
    value = value.strip()

    # Basic allowed characters check
    if not re.match(PHONE_REGEX, value):
        raise BadRequest({
            "error": "Phone may contain digits, spaces, and an optional leading +"
        })

    # Ensure + (plus sign) only appears at the start
    if value.count("+") > 1 or (value.count("+") == 1 and not value.startswith("+")):
        raise BadRequest({
            "error": "Plus sign is only allowed at the beginning"
        })

    # Remove spaces for length check
    digits_only = value.replace(" ", "").lstrip("+")
    if not (7 <= len(digits_only) <= 20):
        raise BadRequest({
            "error": "Phone must contain 7–20 digits (excluding spaces and +)"
        })

    # Return normalized phone number
    normalized = "+" + digits_only if value.startswith("+") else digits_only
    return normalized

def validate_coach_chat(value: str):
    if value is None:
        return None
    value = strip_whitespace(value)
    if value == "":
        return None
    if not (3 <= len(value) <= 50):
        raise BadRequest({"error": "Chat must be between 3 and 50 characters"})
    if not re.match(CHAT_REGEX, value):
        raise BadRequest({"error": "Chat must contain letters or digits and only basic symbols"})
    return value

def validate_coach_bio(value: str) -> str:
    value = value.strip()
    if "<" in value or ">" in value:
        raise BadRequest({"error": "Bio must not contain HTML or script tags"})
    if len(value) > 500:
        raise BadRequest({"error": "Bio is too long"})
    return value

def validate_coach_expertise(value: str) -> str:
    value = value.strip()
    if not re.match(EXPERTISE_REGEX, value):
        raise BadRequest({"error": "Expertise must contain letters and only allowed symbols"})
    return value

def validate_slot(field: str, value: str, min_len: int = 1, max_len: int = 50) -> str:
    if not isinstance(value, str):
        raise BadRequest({"error": f"{field} must be a string"})
    cleaned = value.strip()

    if len(cleaned) < min_len or len(cleaned) > max_len:
        raise BadRequest({"error": f"{field} must be between {min_len} and {max_len} characters"})

    # Allow digits, letters, spaces, colon, hyphen
    if not re.match(r'^[A-Za-z0-9 :\-]+$', cleaned):
        raise BadRequest({
            "error": f"{field} contains invalid characters",
            "allowed": "letters, numbers, spaces, colon, hyphens",
            "value": cleaned
        })
    return cleaned