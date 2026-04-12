# tests/test_constraints.py
# Central definition of all validation rules.
# If a constraint changes, update it here and all tests update automatically.


class NameConstraints:
    """Constraints for name fields across all models."""

    # Coach name constraints
    COACH_FIRSTNAME_MIN = 1
    COACH_FIRSTNAME_MAX = 50
    COACH_LASTNAME_MIN = 1
    COACH_LASTNAME_MAX = 60

    # Startup name constraints
    STARTUP_NAME_MIN = 1
    STARTUP_NAME_MAX = 100
    

    # Boundary test values:
    # test around edges, middle, and well outside for fields with max 50
    BOUNDARY_LENGTHS_50 = [0, 1, 2, 3, 25, 49, 50, 51, 62]
    # for fields with max 60
    BOUNDARY_LENGTHS_60 = [0, 1, 2, 3, 30, 59, 60, 61, 75]
    # well outside test values
    BOUNDARY_LENGTHS_255 = [0, 1, 2, 3, 128, 254, 255, 256, 300]

    # Valid special characters that must be accepted
    VALID_SPECIAL_CHARS = [
        "O'Brien",          # apostrophe
        "Smith-Jones",      # hyphen
        "José",             # Spanish accent
        "Ängström",         # Scandinavian
        "Müller",           # German umlaut
        "Björk",            # Scandinavian
        "Papadópoulos",     # Greek accent
    ]

    # Invalid characters that must be rejected
    INVALID_SPECIAL_CHARS = [
        "<script>",                             # XSS attempt
        "Robert'); DROP TABLE startups;--",     # SQL injection
        "name;name",                            # semicolon
        "name--name",                           # SQL comment
        "<name>",                               # HTML tag
    ]

    UNICODE_NAMES = [
        # European
        "Αλέξανδρος",       # Greek
        "Александр",         # Cyrillic
        "Ångström",          # Scandinavian
        "Müller",            # German umlaut
        "Ó'Brien",           # Irish
        # East Asian
        "普通话",             # Simplified Chinese
        "普通話",             # Traditional Chinese
        "山田太郎",           # Japanese Kanji
        "やまだたろう",        # Japanese Hiragana
        "ヤマダタロウ",        # Japanese Katakana
        "이순신",             # Korean
        # Middle Eastern
        "أحمد",              # Arabic
        "ישראל",             # Hebrew
        "علی",               # Persian/Farsi
        # South Asian
        "अमिताभ",            # Hindi (Devanagari)
        "অমিতাভ",            # Bengali
        "அமிதாப்",           # Tamil
        "అమితాబ్",           # Telugu
        # Southeast Asian
        "สมชาย",             # Thai
        "nguyễn",            # Vietnamese
        # African
        "Ọlọrunfẹmi",        # Yoruba (Nigeria)
        "Ἀχιλλεύς",         # Classical Greek
    ]

    # Names with numbers — must be rejected
    NAMES_WITH_NUMBERS = [
        "John1",
        "2pac",
        "Smith99",
        "1",
        "ABC123",
    ]

class TitleConstraints:
    """Constraints for the Title field in Coaches model.
 
    IMPORTANT: Title is validated by validate_role() which checks FORMAT only,
    not whether the value is in an allowed list. Valid means it matches the
    pattern r"^[\p{L}\p{M}0-9.\-` ']+" and is between 2 and 20 characters.
 
    """
 
    # These are the known valid titles from the codebase
    VALID_TITLES = ["Mr.", "Mrs.", "Ms.", "Miss", "Dr.", "Prof.", "Sir", "Madam", "Coach"]
 
    # These fail because they violate the validate_role pattern or length
    INVALID_TITLES = [
        "",             # empty string — fails min_len=2
        "A",            # too short — fails min_len=2
        "A" * 21,       # too long — fails max_len=20
        "<script>",     # contains < > — fails validate_role pattern
        "Mr!",          # exclamation mark — fails validate_role pattern
        "Dr@",          # @ symbol — fails validate_role pattern
    ]

class EmailConstraints:
    """Constraints for email fields. Using regex validation."""

    MIN = 5
    MAX = 100

    VALID_EMAILS = [
        "user@example.com",
        "user.name@example.com",
        "user+tag@example.co.uk",
        "user123@example.com", 
    ]

    INVALID_EMAILS = [
        "notanemail",           # no @ or domain
        "@nodomain.com",        # no local part
        "noatsign.com",         # no @
        "",                     # empty string
        "a@b.c" * 20,           # way too long
        "user@",                # no domain
        "user@domain",          # no TLD
    ]


class MeetingsConstraints:
    """Constraints for meetings count field."""

    MIN = 0
    # Maximum 20 teams per session
    BOUNDARY_VALUES = [0, 1, 2, 19, 20, 21]


class StatusConstraints:
    """Constraints for startup status field."""

    VALID_VALUES = ["alive", "on-pause", "dead"]
    INVALID_VALUES = ["active", "inactive", "", "ALIVE", "Dead"]


class WebsiteConstraints:
    """Constraints for website URL field."""

    MIN = 5
    MAX = 255

    VALID_URLS = [
        "http://example.com",
        "https://example.com",
        "https://www.example.co.uk",
    ]

    INVALID_URLS = [
        "example.com",          # missing protocol
        "ftp://example.com",    # wrong protocol
        "",                     # empty
        "just text",            # not a URL at all
    ]

class DescriptionConstraints:
    """Constraints for description fields."""
 
    STARTUP_DESCRIPTION_MIN = 0
    STARTUP_DESCRIPTION_MAX = 255
 
    # Boundary values for 255 max length
    BOUNDARY_LENGTHS = [0, 1, 2, 3, 128, 254, 255, 256, 300]

    # validate_startup_description blocks HTML tags
    INVALID_DESCRIPTIONS = [
        "<script>alert('xss')</script>",    # XSS attempt
        "<b>bold</b>",                       # HTML tag
        "A" * 256,                           # too long
    ]


class MemberConstraints:
    """Constraints for startup member fields."""

    NAME_MIN = 2
    NAME_MAX = 100
    EMAIL_MIN = 5
    EMAIL_MAX = 100
    ROLE_MIN = 2
    ROLE_MAX = 50

    VALID_ROLES = ["founder", "co-founder", "CTO", "CEO", "developer"]
    REQUIRED_FIELDS = ["name", "email", "role"]