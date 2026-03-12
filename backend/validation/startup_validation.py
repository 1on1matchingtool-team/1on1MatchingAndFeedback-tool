from .base_validators import *

def validate_startup(data):
    # Required fields
    require_fields(data, [
        "StartupName",
        "Website",
        "Status",
        "PreviousNames",
        "StartupMembers"
    ])

    # StartupName
    validate_string("StartupName", data["StartupName"], min_len=1, max_len=50)

    # Website
    validate_string("Website", data["Website"], min_len=5, max_len=255)
    if not data["Website"].startswith(("http://", "https://")):
        raise BadRequest({"error": "Website must be a valid URL"})

    # Status
    allowed_status = ["alive", "on-pause", "dead"]
    if data["Status"] not in allowed_status:
        raise BadRequest({
            "error": "Invalid Status",
            "allowed": allowed_status
        })

    # PreviousNames (must be a list of strings)
    if not isinstance(data["PreviousNames"], list):
        raise BadRequest({"error": "PreviousNames must be a list"})
    for name in data["PreviousNames"]:
        validate_string("PreviousNames item", name, min_len=1, max_len=50)

    # StartupMembers (must be a list of objects)
    if not isinstance(data["StartupMembers"], list):
        raise BadRequest({"error": "StartupMembers must be a list"})
    if len(data["StartupMembers"]) == 0:
        raise BadRequest({"error": "StartupMembers must have at least one member"})
    for member in data["StartupMembers"]:
        if not isinstance(member, dict):
            raise BadRequest({"error": "Each StartupMember must be an object"})
        require_fields(member, ["name", "email", "role"])
        validate_string("member.name", member["name"], min_len=1, max_len=50)
        validate_string("member.email", member["email"], min_len=5, max_len=100)
        validate_string("member.role", member["role"], min_len=2, max_len=50)

    # Optional fields
    if "StartupSocialMedia" in data and data["StartupSocialMedia"] is not None:
        if not isinstance(data["StartupSocialMedia"], dict):
            raise BadRequest({"error": "StartupSocialMedia must be an object"})

    if "StartupDescription" in data and data["StartupDescription"] is not None:
        validate_string("StartupDescription", data["StartupDescription"], min_len=0, max_len=255)

    if "MeetingsCount" in data:
        validate_int("MeetingsCount", data["MeetingsCount"], min_val=0)
