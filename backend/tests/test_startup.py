import pytest
from werkzeug.exceptions import BadRequest
from backend.tests.test_constraints import (
    NameConstraints,
    StatusConstraints,
    WebsiteConstraints,
)
from backend.validation.startup_validation import validate_startup


# ============================================================
# Category 4 - Hard Constraints
# ============================================================

class TestStartupRequiredFields:
    """Tests that verify required fields cannot be missing."""

    def test_missing_startupname_raises_error(self):
        """A startup cannot be created without a StartupName."""
        data = {
            "Website": "https://example.com",
            "Status": "alive",
            "PreviousNames": [],
            "StartupMembers": [{"name": "Jo", "email": "jo@example.com", "role": "founder"}]
        }
        with pytest.raises(BadRequest) as exc_info:
            validate_startup(data)
        assert "StartupName" in str(exc_info.value)

    def test_missing_website_raises_error(self):
        """A startup cannot be created without a Website."""
        data = {
            "StartupName": "MyStartup",
            "Status": "alive",
            "PreviousNames": [],
            "StartupMembers": [{"name": "Jo", "email": "jo@example.com", "role": "founder"}]
        }
        with pytest.raises(BadRequest) as exc_info:
            validate_startup(data)
        assert "Website" in str(exc_info.value)

    def test_missing_status_raises_error(self):
        """A startup cannot be created without a Status."""
        data = {
            "StartupName": "MyStartup",
            "Website": "https://example.com",
            "PreviousNames": [],
            "StartupMembers": [{"name": "Jo", "email": "jo@example.com", "role": "founder"}]
        }
        with pytest.raises(BadRequest) as exc_info:
            validate_startup(data)
        assert "Status" in str(exc_info.value)

    def test_missing_previousnames_raises_error(self):
        """A startup cannot be created without a PreviousNames field."""
        data = {
            "StartupName": "MyStartup",
            "Website": "https://example.com",
            "Status": "alive",
            "StartupMembers": [{"name": "Jo", "email": "jo@example.com", "role": "founder"}]
        }
        with pytest.raises(BadRequest) as exc_info:
            validate_startup(data)
        assert "PreviousNames" in str(exc_info.value)

    def test_missing_startupmembers_raises_error(self):
        """A startup cannot be created without StartupMembers."""
        data = {
            "StartupName": "MyStartup",
            "Website": "https://example.com",
            "Status": "alive",
            "PreviousNames": []
        }
        with pytest.raises(BadRequest) as exc_info:
            validate_startup(data)
        assert "StartupMembers" in str(exc_info.value)

    def test_empty_startupmembers_raises_error(self):
        """A startup with an empty StartupMembers list should raise a BadRequest."""
        data = {
            "StartupName": "MyStartup",
            "Website": "https://example.com",
            "Status": "alive",
            "PreviousNames": [],
            "StartupMembers": []
        }
        with pytest.raises(BadRequest):
            validate_startup(data)

    def test_all_required_fields_present_passes(self):
        """A startup with all required fields passes validation."""
        data = {
            "StartupName": "MyStartup",
            "Website": "https://example.com",
            "Status": "alive",
            "PreviousNames": [],
            "StartupMembers": [{"name": "Jo", "email": "jo@example.com", "role": "founder"}]
        }
        validate_startup(data)


# ============================================================
# Category 8 - StartupName Boundary Tests
# ============================================================

class TestStartupNameBoundaries:
    """Tests for StartupName length constraints (min=1, max=50)."""

    @pytest.mark.parametrize("length", [
        l for l in NameConstraints.BOUNDARY_LENGTHS_50
        if l >= NameConstraints.STARTUP_NAME_MIN
        and l <= NameConstraints.STARTUP_NAME_MAX
    ])
    def test_valid_startupname_length(self, length):
        """StartupName within allowed length should pass validation."""
        data = {
            "StartupName": "A" * length,
            "Website": "https://example.com",
            "Status": "alive",
            "PreviousNames": [],
            "StartupMembers": [{"name": "Jo", "email": "jo@example.com", "role": "founder"}]
        }
        validate_startup(data)

    @pytest.mark.parametrize("length", [
        l for l in NameConstraints.BOUNDARY_LENGTHS_50
        if l < NameConstraints.STARTUP_NAME_MIN
        or l > NameConstraints.STARTUP_NAME_MAX
    ])
    def test_invalid_startupname_length(self, length):
        """StartupName outside allowed length should fail validation."""
        data = {
            "StartupName": "A" * length,
            "Website": "https://example.com",
            "Status": "alive",
            "PreviousNames": [],
            "StartupMembers": [{"name": "Jo", "email": "jo@example.com", "role": "founder"}]
        }
        with pytest.raises(BadRequest):
            validate_startup(data)


# ============================================================
# Category 8 - Status Constraints
# ============================================================

class TestStartupStatus:
    """Tests for the Status field."""

    @pytest.mark.parametrize("status", StatusConstraints.VALID_VALUES)
    def test_valid_status_accepted(self, status):
        """Valid status values should pass validation."""
        data = {
            "StartupName": "MyStartup",
            "Website": "https://example.com",
            "Status": status,
            "PreviousNames": [],
            "StartupMembers": [{"name": "Jo", "email": "jo@example.com", "role": "founder"}]
        }
        validate_startup(data)

    @pytest.mark.parametrize("status", StatusConstraints.INVALID_VALUES)
    def test_invalid_status_rejected(self, status):
        """Invalid status values should raise a BadRequest."""
        data = {
            "StartupName": "MyStartup",
            "Website": "https://example.com",
            "Status": status,
            "PreviousNames": [],
            "StartupMembers": [{"name": "Jo", "email": "jo@example.com", "role": "founder"}]
        }
        with pytest.raises(BadRequest):
            validate_startup(data)


# ============================================================
# Category 8 - Website Constraints
# ============================================================

class TestStartupWebsite:
    """Tests for the Website field."""

    @pytest.mark.parametrize("url", WebsiteConstraints.VALID_URLS)
    def test_valid_url_accepted(self, url):
        """Valid URLs should pass validation."""
        data = {
            "StartupName": "MyStartup",
            "Website": url,
            "Status": "alive",
            "PreviousNames": [],
            "StartupMembers": [{"name": "Jo", "email": "jo@example.com", "role": "founder"}]
        }
        validate_startup(data)

    @pytest.mark.parametrize("url", WebsiteConstraints.INVALID_URLS)
    def test_invalid_url_rejected(self, url):
        """Invalid URLs should raise a BadRequest."""
        data = {
            "StartupName": "MyStartup",
            "Website": url,
            "Status": "alive",
            "PreviousNames": [],
            "StartupMembers": [{"name": "Jo", "email": "jo@example.com", "role": "founder"}]
        }
        with pytest.raises(BadRequest):
            validate_startup(data)


# ============================================================
# Category 8 - StartupMembers Constraints
# ============================================================

class TestStartupMembers:
    """Tests for the StartupMembers field."""

    def test_members_must_be_a_list(self):
        """StartupMembers must be a list, not a dict or string."""
        data = {
            "StartupName": "MyStartup",
            "Website": "https://example.com",
            "Status": "alive",
            "PreviousNames": [],
            "StartupMembers": {"name": "Jo", "email": "jo@example.com", "role": "founder"}
        }
        with pytest.raises(BadRequest):
            validate_startup(data)

    def test_member_missing_name_raises_error(self):
        """A member without a name should raise a BadRequest."""
        data = {
            "StartupName": "MyStartup",
            "Website": "https://example.com",
            "Status": "alive",
            "PreviousNames": [],
            "StartupMembers": [{"email": "jo@example.com", "role": "founder"}]
        }
        with pytest.raises(BadRequest):
            validate_startup(data)

    def test_member_missing_email_raises_error(self):
        """A member without an email should raise a BadRequest."""
        data = {
            "StartupName": "MyStartup",
            "Website": "https://example.com",
            "Status": "alive",
            "PreviousNames": [],
            "StartupMembers": [{"name": "Jo", "role": "founder"}]
        }
        with pytest.raises(BadRequest):
            validate_startup(data)

    def test_member_missing_role_raises_error(self):
        """A member without a role should raise a BadRequest."""
        data = {
            "StartupName": "MyStartup",
            "Website": "https://example.com",
            "Status": "alive",
            "PreviousNames": [],
            "StartupMembers": [{"name": "Jo", "email": "jo@example.com"}]
        }
        with pytest.raises(BadRequest):
            validate_startup(data)

    def test_multiple_members_all_valid_passes(self):
        """A startup with multiple valid members should pass validation."""
        data = {
            "StartupName": "MyStartup",
            "Website": "https://example.com",
            "Status": "alive",
            "PreviousNames": [],
            "StartupMembers": [
                {"name": "Jo", "email": "jo@example.com", "role": "founder"},
                {"name": "Mary Jane", "email": "mary@example.com", "role": "CTO"},
                {"name": "Ali", "email": "ali@example.com", "role": "developer"}
            ]
        }
        validate_startup(data)

    def test_one_invalid_member_among_valid_ones_raises_error(self):
        """If one member is invalid the whole request should be rejected,
        even if all other members are valid."""
        data = {
            "StartupName": "MyStartup",
            "Website": "https://example.com",
            "Status": "alive",
            "PreviousNames": [],
            "StartupMembers": [
                {"name": "Jo", "email": "jo@example.com", "role": "founder"},      # valid
                {"name": "Mary Jane", "email": "mary@example.com", "role": "CTO"}, # valid
                {"name": "Bad1Name", "email": "bad@example.com", "role": "developer"} # invalid
            ]
        }
        with pytest.raises(BadRequest):
            validate_startup(data)

    def test_member_name_with_numbers_rejected(self):
        """A member name containing numbers should raise a BadRequest."""
        data = {
            "StartupName": "MyStartup",
            "Website": "https://example.com",
            "Status": "alive",
            "PreviousNames": [],
            "StartupMembers": [{"name": "Jo1", "email": "jo@example.com", "role": "founder"}]
        }
        with pytest.raises(BadRequest):
            validate_startup(data)


# ============================================================
# Category 8 - PreviousNames Constraints
# ============================================================

class TestStartupPreviousNames:
    """Tests for the PreviousNames field."""

    def test_previousnames_must_be_a_list(self):
        """PreviousNames must be a list, not a string."""
        data = {
            "StartupName": "MyStartup",
            "Website": "https://example.com",
            "Status": "alive",
            "PreviousNames": "OldName",
            "StartupMembers": [{"name": "Jo", "email": "jo@example.com", "role": "founder"}]
        }
        with pytest.raises(BadRequest):
            validate_startup(data)

    def test_empty_previousnames_passes(self):
        """An empty PreviousNames list should pass validation."""
        data = {
            "StartupName": "MyStartup",
            "Website": "https://example.com",
            "Status": "alive",
            "PreviousNames": [],
            "StartupMembers": [{"name": "Jo", "email": "jo@example.com", "role": "founder"}]
        }
        validate_startup(data)

    def test_previousnames_with_valid_strings_passes(self):
        """PreviousNames with valid string entries should pass validation."""
        data = {
            "StartupName": "MyStartup",
            "Website": "https://example.com",
            "Status": "alive",
            "PreviousNames": ["OldName", "AnotherOldName"],
            "StartupMembers": [{"name": "Jo", "email": "jo@example.com", "role": "founder"}]
        }
        validate_startup(data)

    def test_previousnames_item_too_long_raises_error(self):
        """A PreviousNames item exceeding max length should raise a BadRequest."""
        data = {
            "StartupName": "MyStartup",
            "Website": "https://example.com",
            "Status": "alive",
            "PreviousNames": ["A" * 51],
            "StartupMembers": [{"name": "Jo", "email": "jo@example.com", "role": "founder"}]
        }
        with pytest.raises(BadRequest):
            validate_startup(data)


# ============================================================
# Category 8 - Unicode in Startup Names
# ============================================================

class TestStartupNameUnicode:
    """Tests that valid Unicode characters are accepted in startup names."""

    @pytest.mark.parametrize("name", NameConstraints.UNICODE_NAMES)
    def test_unicode_startupname_accepted(self, name):
        """Unicode characters should be accepted in StartupName."""
        data = {
            "StartupName": name,
            "Website": "https://example.com",
            "Status": "alive",
            "PreviousNames": [],
            "StartupMembers": [{"name": "Jo", "email": "jo@example.com", "role": "founder"}]
        }
        validate_startup(data)