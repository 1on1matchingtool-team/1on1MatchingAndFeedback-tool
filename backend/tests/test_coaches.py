# Tests for coach validation and model constraints.
#
# IMPORTANT NOTES:
# 1. auto_split_person_name() currently runs BEFORE validation in
#    validate_coach() and mutates data. Tests here treat FirstName and LastName as separate
#    fields and do not test auto-split behavior.
#
# 2. validate_email() raises ValueError not BadRequest.
#    Email tests catch both to be safe.
#
# 3. Title is validated by validate_role() — format only, not allowed list.
#    Any string matching the role pattern and within length passes.

import pytest
from werkzeug.exceptions import BadRequest
from backend.tests.test_constraints import NameConstraints, EmailConstraints, TitleConstraints
from backend.validation.coach_validation import validate_coach


# ============================================================
# Category 4 - Hard Constraints
# ============================================================

class TestCoachRequiredFields:
    """Tests that verify required fields cannot be missing."""

    def test_missing_firstname_raises_error(self):
        """A coach cannot be created without a FirstName."""
        data = {
            "LastName": "Smith",
            "Email": "smith@example.com"
        }
        with pytest.raises(BadRequest) as exc_info:
            validate_coach(data)
        assert "FirstName" in str(exc_info.value)

    def test_missing_lastname_raises_error(self):
        """A coach cannot be created without a LastName."""
        data = {
            "FirstName": "John",
            "Email": "john@example.com"
        }
        with pytest.raises(BadRequest) as exc_info:
            validate_coach(data)
        assert "LastName" in str(exc_info.value)

    def test_missing_email_raises_error(self):
        """A coach cannot be created without an Email."""
        data = {
            "FirstName": "John",
            "LastName": "Smith"
        }
        with pytest.raises((BadRequest, ValueError)):
            validate_coach(data)

    def test_all_required_fields_present_passes(self):
        """A coach with all required fields passes validation."""
        data = {
            "FirstName": "John",
            "LastName": "Smith",
            "Email": "john.smith@example.com"
        }
        validate_coach(data)

    def test_unknown_field_raises_error(self):
        """Sending an unknown field should raise a BadRequest."""
        data = {
            "FirstName": "John",
            "LastName": "Smith",
            "Email": "john@example.com",
            "UnknownField": "something"
        }
        with pytest.raises(BadRequest) as exc_info:
            validate_coach(data)
        assert "Unknown field" in str(exc_info.value)


# ============================================================
# Category 4 - PATCH vs POST
# ============================================================

class TestCoachPatchVsPost:
    """Tests that verify POST and PATCH behave differently."""

    def test_patch_with_single_field_passes(self):
        """A PATCH request with just one valid field should pass."""
        data = {"FirstName": "John"}
        validate_coach(data, is_patch=True)

    def test_patch_with_no_valid_fields_raises_error(self):
        """A PATCH request with no valid fields should raise a BadRequest."""
        data = {}
        with pytest.raises(BadRequest):
            validate_coach(data, is_patch=True)

    def test_post_without_required_fields_raises_error(self):
        """A POST request missing required fields should raise a BadRequest."""
        data = {"FirstName": "John"}
        with pytest.raises(BadRequest):
            validate_coach(data, is_patch=False)


# ============================================================
# Category 8 - Title Constraints
# ============================================================

class TestCoachTitle:
    """Tests for the optional Title field.

    Note: Title is validated by validate_role() which checks FORMAT only.
    Valid titles are those matching r"^[\p{L}\p{M}0-9.\-` ']+"
    and between 2 and 20 characters.
    """

    @pytest.mark.parametrize("title", TitleConstraints.VALID_TITLES)
    def test_valid_title_accepted(self, title):
        """Valid titles should pass validation."""
        data = {
            "FirstName": "John",
            "LastName": "Smith",
            "Email": "john@example.com",
            "Title": title
        }
        validate_coach(data)

    @pytest.mark.parametrize("title", TitleConstraints.INVALID_TITLES)
    def test_invalid_title_rejected(self, title):
        """Invalid titles should raise a BadRequest."""
        data = {
            "FirstName": "John",
            "LastName": "Smith",
            "Email": "john@example.com",
            "Title": title
        }
        with pytest.raises(BadRequest):
            validate_coach(data)

    def test_missing_title_passes(self):
        """Title is optional — omitting it should pass validation."""
        data = {
            "FirstName": "John",
            "LastName": "Smith",
            "Email": "john@example.com"
        }
        validate_coach(data)

    def test_none_title_passes(self):
        """Title set to None should pass validation since it is optional."""
        data = {
            "FirstName": "John",
            "LastName": "Smith",
            "Email": "john@example.com",
            "Title": None
        }
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
    def test_valid_firstname_length(self, length):
        """FirstName within allowed length should pass validation."""
        data = {
            "FirstName": "A" * length,
            "LastName": "Smith",
            "Email": "test@example.com"
        }
        validate_coach(data)

    @pytest.mark.parametrize("length", [
        l for l in NameConstraints.BOUNDARY_LENGTHS_50
        if l < NameConstraints.COACH_FIRSTNAME_MIN
        or l > NameConstraints.COACH_FIRSTNAME_MAX
    ])
    def test_invalid_firstname_length(self, length):
        """FirstName outside allowed length should fail validation."""
        data = {
            "FirstName": "A" * length,
            "LastName": "Smith",
            "Email": "test@example.com"
        }
        with pytest.raises(BadRequest):
            validate_coach(data)

    @pytest.mark.parametrize("name", NameConstraints.NAMES_WITH_NUMBERS)
    def test_firstname_with_numbers_rejected(self, name):
        """FirstName containing numbers should fail validation."""
        data = {
            "FirstName": name,
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
    def test_valid_lastname_length(self, length):
        """LastName within allowed length should pass validation."""
        data = {
            "FirstName": "John",
            "LastName": "A" * length,
            "Email": "test@example.com"
        }
        validate_coach(data)

    @pytest.mark.parametrize("length", [
        l for l in NameConstraints.BOUNDARY_LENGTHS_60
        if l < NameConstraints.COACH_LASTNAME_MIN
        or l > NameConstraints.COACH_LASTNAME_MAX
    ])
    def test_invalid_lastname_length(self, length):
        """LastName outside allowed length should fail validation."""
        data = {
            "FirstName": "John",
            "LastName": "A" * length,
            "Email": "test@example.com"
        }
        with pytest.raises(BadRequest):
            validate_coach(data)

    @pytest.mark.parametrize("name", NameConstraints.NAMES_WITH_NUMBERS)
    def test_lastname_with_numbers_rejected(self, name):
        """LastName containing numbers should fail validation."""
        data = {
            "FirstName": "John",
            "LastName": name,
            "Email": "test@example.com"
        }
        with pytest.raises(BadRequest):
            validate_coach(data)


# ============================================================
# Category 8 - Email Constraints
# ============================================================

class TestCoachEmailConstraints:
    """Tests for Email field constraints.

    Note: validate_email() raises ValueError not BadRequest.
    Tests catch both to be safe.
    """

    @pytest.mark.parametrize("email", EmailConstraints.VALID_EMAILS)
    def test_valid_email_accepted(self, email):
        """Valid emails should pass validation."""
        data = {
            "FirstName": "John",
            "LastName": "Smith",
            "Email": email
        }
        validate_coach(data)

    @pytest.mark.parametrize("email", EmailConstraints.INVALID_EMAILS)
    def test_invalid_email_rejected(self, email):
        """Invalid emails should raise an error."""
        data = {
            "FirstName": "John",
            "LastName": "Smith",
            "Email": email
        }
        with pytest.raises((BadRequest, ValueError)):
            validate_coach(data)


# ============================================================
# Category 8 - Unicode and Special Characters
# ============================================================

class TestCoachNameUnicode:
    """Tests that valid Unicode characters are accepted in names."""

    @pytest.mark.parametrize("name", NameConstraints.UNICODE_NAMES)
    def test_unicode_firstname_accepted(self, name):
        """Unicode characters should be accepted in FirstName."""
        data = {
            "FirstName": name,
            "LastName": "Smith",
            "Email": "test@example.com"
        }
        validate_coach(data)

    @pytest.mark.parametrize("name", NameConstraints.UNICODE_NAMES)
    def test_unicode_lastname_accepted(self, name):
        """Unicode characters should be accepted in LastName."""
        data = {
            "FirstName": "John",
            "LastName": name,
            "Email": "test@example.com"
        }
        validate_coach(data)

    @pytest.mark.parametrize("name", NameConstraints.VALID_SPECIAL_CHARS)
    def test_valid_special_chars_accepted(self, name):
        """Valid special characters like hyphens and apostrophes
        should be accepted in names."""
        data = {
            "FirstName": name,
            "LastName": "Smith",
            "Email": "test@example.com"
        }
        validate_coach(data)

    @pytest.mark.parametrize("name", NameConstraints.INVALID_SPECIAL_CHARS)
    def test_invalid_special_chars_rejected(self, name):
        """Dangerous characters should be rejected."""
        data = {
            "FirstName": name,
            "LastName": "Smith",
            "Email": "test@example.com"
        }
        with pytest.raises(BadRequest):
            validate_coach(data)