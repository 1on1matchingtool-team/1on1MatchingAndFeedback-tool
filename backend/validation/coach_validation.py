from .base_validators import *
from werkzeug.exceptions import BadRequest

def validate_coach(data, is_patch=False):
    # Allowed fields
    ALLOWED_FIELDS = {
        "Title",
        "FirstName",
        "LastName",
        "Email",
        "Phone",
        "Chat",
        "Bio",
        "Expertise",
        "SocialMedia",
        "CoachingSessions",
        "BatchesCoached"
    }

    # Reject unknown fields
    for key in data.keys():
        if key not in ALLOWED_FIELDS:
            raise BadRequest({"error": f"Unknown field: {key}"})

    # Required fields for POSTh
    if not is_patch:
        REQUIRED_FIELDS = ["FirstName", "LastName", "Email"]
        require_fields(data, REQUIRED_FIELDS)
    else:
        # PATCH: must include at least one valid field
        if not any(field in data for field in ALLOWED_FIELDS):
            raise BadRequest({"error": "No valid fields provided for update"})

    # Collect warnings
    warnings = []

    # --------------------
    # Field validations
    # --------------------

    # Title (optional, letters/numbers/spaces/hyphens) - Might remove later and be implemented in the frontend
    if "Title" in data and data["Title"] is not None:
        cleaned = strip_whitespace(data["Title"])
        validate_string("Title", cleaned, min_len=2, max_len=20)
        validate_role("Title", cleaned)
        data["Title"] = cleaned

    # FirstName (Unicode allowed)
    if "FirstName" in data:
        cleaned = strip_whitespace(data["FirstName"])
        validate_person_name("FirstName", cleaned, min_len=1, max_len=50)
        data["FirstName"] = cleaned

    # LastName (Unicode allowed)
    if "LastName" in data:
        cleaned = strip_whitespace(data["LastName"])
        validate_person_name("LastName", cleaned, min_len=1, max_len=60)
        data["LastName"] = cleaned

    # Email
    if "Email" in data:
        data["Email"] = validate_email("Email", data["Email"])

    # Phone (free text but no emojis)
    if "Phone" in data:
        data["Phone"] = validate_coach_phone(data["Phone"])

    # Chat (free text but no emojis)
    if "Chat" in data:
        data["Chat"] = validate_coach_chat(data["Chat"])

    # Bio (free text, emojis allowed)
    if "Bio" in data:
        data["Bio"] = validate_coach_bio(data["Bio"])

    # Expertise (free text, emojis allowed)
    if "Expertise" in data:
        data["Expertise"] = validate_coach_expertise(data["Expertise"])

    # SocialMedia (flexible + normalize)
    if "SocialMedia" in data:
        cleaned, w = validate_social_media_flexible(data["SocialMedia"])
        data["SocialMedia"] = cleaned
        warnings.extend(w)

    # CoachingSessions
    if "CoachingSessions" in data:
        validate_int("CoachingSessions", data["CoachingSessions"], min_val=0)

    # BatchesCoached
    if "BatchesCoached" in data:
        validate_int("BatchesCoached", data["BatchesCoached"], min_val=0)

    return data, warnings