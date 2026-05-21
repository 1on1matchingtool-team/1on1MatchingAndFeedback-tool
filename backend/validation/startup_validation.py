from .base_validators import *
from werkzeug.exceptions import BadRequest
from urllib.parse import urlparse
import re

# Updated Website validator (warning-based, not strict reject)
def validate_website_with_warnings(value):
    warnings = []
    v = strip_whitespace(value)

    if not v:
        raise BadRequest({"error": "Website is required"})

    # Block unsafe schemes
    if v.lower().startswith(("javascript:", "data:", "file:")):
        raise BadRequest({"error": "Website contains an unsafe URL"})

    # Block script injection
    if "<script>" in v.lower() or "</script>" in v.lower():
        raise BadRequest({"error": "Website contains script injection"})

    # Warn if http instead of https
    if v.startswith("http://"):
        warnings.append("Website uses http instead of https (not recommended).")

    # Warn if missing scheme
    if not v.startswith(("http://", "https://")):
        warnings.append("Website has no scheme (http/https). Accepted as placeholder.")

    # Validate structure if scheme exists
    if v.startswith(("http://", "https://")):
        parsed = urlparse(v)
        if not parsed.netloc:
            raise BadRequest({"error": "Website must contain a valid domain"})

    # Warn if no dot
    if "." not in v:
        warnings.append("Website may not be a valid domain. Accepted as placeholder.")

    return v, warnings

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

    # Collect warnings
    warnings = []

    # --------------------
    # Field validations
    # --------------------

    # StartupName (Unicode, numbers, and symbols allowed)
    if "StartupName" in data:
        cleaned = strip_whitespace(data["StartupName"])
        validate_startup_name("StartupName", cleaned, min_len=1, max_len=100)
        data["StartupName"] = cleaned

    # Website (warning-based)
    if "Website" in data:
        cleaned, w = validate_website_with_warnings(data["Website"])
        data["Website"] = cleaned
        warnings.extend(w)

    # Status
    if "Status" in data:
        allowed_status = ["alive", "on-pause", "dead"]
        if data["Status"] not in allowed_status:
            raise BadRequest({"error": "Invalid Status","allowed": allowed_status})

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

        # Enforce at least 1 member on POST
        if not is_patch and len(data["StartupMembers"]) == 0:
            raise BadRequest({"error": "Startup must have at least 1 member"})

        cleaned_members = []
        for member in data["StartupMembers"]:
            if not isinstance(member, dict):
                raise BadRequest({"error": "Each StartupMember must be an object"})
            require_fields(member, ["name", "email", "role"])

            # Name (Unicode allowed)
            cleaned_name = strip_whitespace(member["name"])
            validate_person_name("member.name", cleaned_name, min_len=2, max_len=100)

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

    # StartupSocialMedia (flexible + normalize)
    if "StartupSocialMedia" in data:
        cleaned, w = validate_social_media_flexible(data["StartupSocialMedia"])
        data["StartupSocialMedia"] = cleaned
        warnings.extend(w)

    # StartupDescription (free text, emojis allowed)
    if "StartupDescription" in data and data["StartupDescription"] is not None:
        data["StartupDescription"] = validate_startup_description(data["StartupDescription"])

    # MeetingsCount (int)
    if "MeetingsCount" in data:
        validate_int("MeetingsCount", data["MeetingsCount"], min_val=0)

    return data, warnings