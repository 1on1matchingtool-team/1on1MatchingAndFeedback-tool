from .base_validators import *
from werkzeug.exceptions import BadRequest

def validate_startup(data, is_patch=False):
    # Allowed fields
    ALLOWED_FIELDS = {
        "StartupName",
        "Website",
        "Status",
        "PreviousNames",
        "StartupMembers",
        "StartupSocialMedia",
        "StartupDescription",
        "MeetingsCount"
    }

    # Reject unknown fields
    for key in data.keys():
        if key not in ALLOWED_FIELDS:
            raise BadRequest({"error": f"Unknown field: {key}"})

   # Required fields for POST
    if not is_patch:
        REQUIRED_FIELDS = [
            "StartupName",
            "Website",
            "Status",
            "PreviousNames",
            "StartupMembers"
        ]
        require_fields(data, REQUIRED_FIELDS)
    else:
        # PATCH must include at least one valid field
        if not any(field in data for field in ALLOWED_FIELDS):
            raise BadRequest({"error": "No valid fields provided for update"})

    # --------------------
    # Field validations
    # --------------------

    # StartupName (Unicode, numbers, and symbols allowed)
    if "StartupName" in data:
        cleaned = strip_whitespace(data["StartupName"])
        validate_startup_name("StartupName", cleaned, min_len=1, max_len=100)
        data["StartupName"] = cleaned

    # Website
    if "Website" in data:
        cleaned = strip_whitespace(data["Website"])
        validate_string("Website", cleaned, min_len=5, max_len=255)

        if not cleaned.startswith(("http://", "https://")):
            raise BadRequest({"error": "Website must start with http:// or https://"})
        data["Website"] = cleaned

    # Status
    if "Status" in data:
        allowed_status = ["alive", "on-pause", "dead"]
        if data["Status"] not in allowed_status:
            raise BadRequest({
                "error": "Invalid Status",
                "allowed": allowed_status
            })

    # PreviousNames (list of strings)
    if "PreviousNames" in data:
        if not isinstance(data["PreviousNames"], list):
            raise BadRequest({"error": "PreviousNames must be a list"})

        cleaned_prev = []
        for name in data["PreviousNames"]:
            cleaned = strip_whitespace(name)
            validate_startup_name("PreviousNames item", cleaned, min_len=1, max_len=100)
            cleaned_prev.append(cleaned)
        data["PreviousNames"] = cleaned_prev

    # StartupMembers (list of objects)
    if "StartupMembers" in data:
        if not isinstance(data["StartupMembers"], list):
            raise BadRequest({"error": "StartupMembers must be a list"})

        cleaned_members = []
        for member in data["StartupMembers"]:
            if not isinstance(member, dict):
                raise BadRequest({"error": "Each StartupMember must be an object"})
            require_fields(member, ["name", "email", "role"])

            # Name (Unicode allowed)
            cleaned_name = strip_whitespace(member["name"])
            validate_unicode_name("member.name", cleaned_name, min_len=2, max_len=100)

            # Email
            cleaned_email = strip_whitespace(member["email"])
            validate_email("member.email", cleaned_email)

            # Role (letters, numbers, spaces, and hyphens)
            cleaned_role = strip_whitespace(member["role"])
            validate_role("member.role", cleaned_role, min_len=2, max_len=50)

            cleaned_members.append({
                "name": cleaned_name,
                "email": cleaned_email,
                "role": cleaned_role
            })

        data["StartupMembers"] = cleaned_members

    # StartupSocialMedia
    if "StartupSocialMedia" in data and data["StartupSocialMedia"] is not None:
        validate_social_media("StartupSocialMedia", data["StartupSocialMedia"])

    # StartupDescription (free text, emojis allowed)
    if "StartupDescription" in data and data["StartupDescription"] is not None:
        data["StartupDescription"] = validate_startup_description(data["StartupDescription"])

    # MeetingsCount (int)
    if "MeetingsCount" in data:
        validate_int("MeetingsCount", data["MeetingsCount"], min_val=0)

    return data