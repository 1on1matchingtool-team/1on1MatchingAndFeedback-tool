from .base_validators import *

def validate_coach(data):
    # Required fields
    require_fields(data, ["FirstName", "LastName", "Email"])

    # FirstName
    validate_string("FirstName", data["FirstName"], min_len=1, max_len=50)

    # LastName
    validate_string("LastName", data["LastName"], min_len=1, max_len=60)

    # Email
    validate_string("Email", data["Email"], min_len=5, max_len=100)
    if "@" not in data["Email"] or "." not in data["Email"]:
        raise BadRequest({
            "error": "Invalid email format",
            "value": data["Email"]
        })

    # Optional: Phone
    if "Phone" in data and data["Phone"] is not None:
        validate_string("Phone", data["Phone"], min_len=3, max_len=100)

    # Optional: Chat
    if "Chat" in data and data["Chat"] is not None:
        validate_string("Chat", data["Chat"], min_len=2, max_len=100)

    # Optional: Bio
    if "Bio" in data and data["Bio"] is not None:
        validate_string("Bio", data["Bio"], min_len=0, max_len=500)

    # Optional: Expertise
    if "Expertise" in data and data["Expertise"] is not None:
        validate_string("Expertise", data["Expertise"], min_len=2, max_len=200)

    # Optional: SocialMedia (must be a dict)
    if "SocialMedia" in data and data["SocialMedia"] is not None:
        if not isinstance(data["SocialMedia"], dict):
            raise BadRequest({"error": "SocialMedia must be an object"})

    # Optional: CoachingSessions
    if "CoachingSessions" in data:
        validate_int("CoachingSessions", data["CoachingSessions"], min_val=0)

    # Optional: BatchesCoached
    if "BatchesCoached" in data:
        validate_int("BatchesCoached", data["BatchesCoached"], min_val=0)