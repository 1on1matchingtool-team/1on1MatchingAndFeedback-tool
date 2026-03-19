
import pytest
from werkzeug.exceptions import BadRequest
from backend.tests.factories import CoachFactory
from backend.tests.test_constraints import NameConstraints, EmailConstraints
from backend.validation.coach_validation import validate_coach

# Category 4 - Hard Constraints

class TestCoachRequiredFields:
    """Tests that verify required fields cannot be missing."""

    def test_missing_firstname_raises_error(self, db_session):
        """A coach cannot be created without a FirstName."""
        data = {
            "LastName": "Smith",
            "Email": "smith@example.com"
        }
        with pytest.raises(BadRequest) as exc_info:
            validate_coach(data)
        assert "FirstName" in str(exc_info.value)

    def test_missing_lastname_raises_error(self, db_session):
        """A coach cannot be created without a LastName."""
        data = {
            "FirstName": "John",
            "Email": "john@example.com"
        }
        with pytest.raises(BadRequest) as exc_info:
            validate_coach(data)
        assert "LastName" in str(exc_info.value)

    def test_missing_email_raises_error(self, db_session):
        """A coach cannot be created without an Email."""
        data = {
            "FirstName": "John",
            "LastName": "Smith"
        }
        with pytest.raises(BadRequest) as exc_info:
            validate_coach(data)
        assert "Email" in str(exc_info.value)

    def test_all_required_fields_present_passes(self, db_session):
        """A coach with all required fields passes validation."""
        data = {
            "FirstName": "John",
            "LastName": "Smith",
            "Email": "john.smith@example.com"
        }
        # Should not raise any exception
        validate_coach(data)


# ============================================================
# Category 8 - Boundary Value Tests
# ============================================================

class TestCoachFirstNameBoundaries:
    """Tests for FirstName length constraints (min=1, max=50)."""

    @pytest.mark.parametrize("length", [
        l for l in NameConstraints.BOUNDARY_LENGTHS_50
        if l >= NameConstraints.COACH_FIRSTNAME_MIN
        and l <= NameConstraints.COACH_FIRSTNAME_MAX
    ])
    def test_valid_firstname_length(self, db_session, length):
        """FirstName within allowed length should pass validation."""
        data = {
            "FirstName": "A" * length,
            "LastName": "Smith",
            "Email": "test@example.com"
        }
        validate_coach(data)  # should not raise

    @pytest.mark.parametrize("length", [
        l for l in NameConstraints.BOUNDARY_LENGTHS_50
        if l < NameConstraints.COACH_FIRSTNAME_MIN
        or l > NameConstraints.COACH_FIRSTNAME_MAX
    ])
    def test_invalid_firstname_length(self, db_session, length):
        """FirstName outside allowed length should fail validation."""
        data = {
            "FirstName": "A" * length,
            "LastName": "Smith",
            "Email": "test@example.com"
        }
        with pytest.raises(BadRequest):
            validate_coach(data)


class TestCoachLastNameBoundaries:
    """Tests for LastName length constraints (min=1, max=60)."""

    @pytest.mark.parametrize("length", [
        l for l in NameConstraints.BOUNDARY_LENGTHS_60
        if l >= NameConstraints.COACH_LASTNAME_MIN
        and l <= NameConstraints.COACH_LASTNAME_MAX
    ])
    def test_valid_lastname_length(self, db_session, length):
        """LastName within allowed length should pass validation."""
        data = {
            "FirstName": "John",
            "LastName": "A" * length,
            "Email": "test@example.com"
        }
        validate_coach(data)  # should not raise

    @pytest.mark.parametrize("length", [
        l for l in NameConstraints.BOUNDARY_LENGTHS_60
        if l < NameConstraints.COACH_LASTNAME_MIN
        or l > NameConstraints.COACH_LASTNAME_MAX
    ])
    def test_invalid_lastname_length(self, db_session, length):
        """LastName outside allowed length should fail validation."""
        data = {
            "FirstName": "John",
            "LastName": "A" * length,
            "Email": "test@example.com"
        }
        with pytest.raises(BadRequest):
            validate_coach(data)


# ============================================================
# Category 8 - Unicode and Special Characters
# ============================================================

class TestCoachNameUnicode:
    """Tests that valid Unicode characters are accepted in names."""

    @pytest.mark.parametrize("name", NameConstraints.UNICODE_NAMES)
    def test_unicode_firstname_accepted(self, db_session, name):
        """Unicode characters should be accepted in FirstName."""
        data = {
            "FirstName": name,
            "LastName": "Smith",
            "Email": "test@example.com"
        }
        validate_coach(data)  # should not raise

    @pytest.mark.parametrize("name", NameConstraints.VALID_SPECIAL_CHARS)
    def test_valid_special_chars_accepted(self, db_session, name):
        """Valid special characters like hyphens and apostrophes should be accepted."""
        data = {
            "FirstName": name,
            "LastName": "Smith",
            "Email": "test@example.com"
        }
        validate_coach(data)  # should not raise

    @pytest.mark.parametrize("name", NameConstraints.INVALID_SPECIAL_CHARS)
    def test_invalid_special_chars_rejected(self, db_session, name):
        """Dangerous characters should be rejected."""
        data = {
            "FirstName": name,
            "LastName": "Smith",
            "Email": "test@example.com"
        }
        with pytest.raises(BadRequest):
            validate_coach(data)