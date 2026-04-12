import regex as re
from datetime import datetime
from werkzeug.exceptions import BadRequest
from urllib.parse import urlparse

# --------------------------------------
# Constants (Group all titles and regex)
# --------------------------------------

TITLES = {

    "mr", "mr.", "mrs", "mrs.", "ms", "ms.", "miss",
    "dr", "dr.", "prof", "prof.", "sir", "madam", "coach"
}
TITLES_WITH_DOT = {"mr", "mrs", "ms", "dr", "prof"}
NAME_ALLOWED_REGEX = r"^[\p{L}’'\- ]+$"
PHONE_REGEX = r"^[0-9]{7,20}$"
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

def validate_unicode_name(field, value, min_len=1, max_len=100):
    value = strip_whitespace(value)
    validate_string(field, value, min_len, max_len)
    pattern = r"^[\p{L}\p{M}'\- ]+$"

    try:
        import regex as reg
        if not reg.match(pattern, value):
            raise BadRequest({
                "error": f"{field} contains invalid characters",
                "allowed": "Unicode letters, accents, hyphens, apostrophes, spaces",
                "value": value
            })
    except ImportError:
        # Fallback: basic unicode letter check
        for ch in value:
            if ch.isalpha() or ch in ["'", "-", " "]:
                continue
            raise BadRequest({
                "error": f"{field} contains invalid characters",
                "value": value
            })

    return value

def validate_startup_name(field, value, min_len=1, max_len=100):
    value = strip_whitespace(value)
    validate_string(field, value, min_len, max_len)

    pattern = r"^[\p{L}\p{M}0-9 ._+\-]+$"

    try:
        import regex as reg
        if not reg.match(pattern, value):
            raise BadRequest({
                "error": f"{field} contains invalid characters",
                "allowed": "Unicode letters, numbers, spaces, hyphens, underscores, dots, plus signs",
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

def validate_social_media(field_name: str, sm: dict) -> dict:
    if not isinstance(sm, dict):
        raise BadRequest({"error": f"{field_name} must be an object"})
    cleaned = {}

    for key, value in sm.items():
        if not isinstance(value, str):
            raise BadRequest({"error": f"{field_name}.{key} must be a string"})
        v = value.strip()

        # Block javascript URLs
        if v.lower().startswith("javascript:"):
            raise BadRequest({"error": f"{field_name}.{key} contains an unsafe URL"})
        parsed = urlparse(v)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise BadRequest({"error": f"{field_name}.{key} must be a valid URL"})
        cleaned[key] = v

    return cleaned

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

def insert_spaces_if_missing(name):
    # Insert space between lowercase to Uppercase
    name = re.sub(r"([a-z])([A-Z])", r"\1 \2", name)
    # Insert space after title
    name = re.sub(r"(Mr|Mrs|Ms|Miss|Dr|Prof|Coach)\.?", r"\1 ", name, flags=re.IGNORECASE)
    return name

def remove_invalid_symbols(text):
    # Keep letters, numbers, spaces, hyphens, apostrophes
    return re.sub(r"[^A-Za-z0-9 '\-]", "", text)

# ---------------------
# Name splitting logic
# ---------------------
def auto_split_person_name(first_name, last_name):
    title = None
    raw_title = ""
    # 1. Process FirstName
    if first_name:
        fn = normalize_name(first_name)
        fn = insert_spaces_if_missing(fn)

        # Validate before cleaning
        validate_name_characters("FirstName", fn)

        fn = remove_invalid_symbols(fn)
        parts = fn.split()

        if not parts:
            first_name = ""
        else:
            # Detect title
            first_token = parts[0].lower()
            if first_token in TITLES:
                raw_title = parts[0].capitalize().rstrip(".")

                # Add dot only for abbreviations
                if first_token in TITLES_WITH_DOT:
                    title = raw_title + "."
                else:
                    title = raw_title
                parts = parts[1:]

            # FirstName = first remaining token
            if parts:
                first_name = parts[0].capitalize()
            else:
                first_name = raw_title if title else ""
    else:
        first_name = ""

    # 2. Process LastName
    if last_name:
        ln = normalize_name(last_name)
        ln = insert_spaces_if_missing(ln)

        # Validate before cleaning
        validate_name_characters("LastName", ln)

        ln = remove_invalid_symbols(ln)
        parts = ln.split()

        # Remove duplicate first name
        if parts and first_name and parts[0].lower() == first_name.lower():
            parts = parts[1:]

        # Capitalize each part
        last_name = " ".join([p.capitalize() for p in parts])
    else:
        last_name = ""
    return title, first_name, last_name

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
    if not (7 <= len(value) <= 20):
        raise BadRequest({"error": "Phone must be between 7 and 20 digits long"})
    if not value.isdigit():
        raise BadRequest({"error": "Phone must contain digits only"})
    return value

def validate_coach_chat(value: str) -> str:
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