# Tests for basic assignment behaviour — breaks, single coach/startup,
# and empty slots when no startups are available.

from backend.algo import assign_startups_to_coaches


class TestBreaksPreserved:
    """Tests that verify break slots are never overwritten with a startup."""

    def test_break_slot_is_marked_as_break(self, coach_with_break):
        """A break slot must always appear as Break in the assignments,
        never replaced by a startup."""
        coaches, startups, feedbacks = coach_with_break
        result = assign_startups_to_coaches(coaches, startups, feedbacks)

        assignments = result["Coach Bob"]["Assignments"]
        break_assignments = [a for a in assignments if a["Slot"] == "Break"]

        assert len(break_assignments) == 1, (
            "Expected exactly one Break slot in assignments"
        )
        assert break_assignments[0]["Startup_name"] == "Break", (
            "Break slot must be marked as Break, not filled with a startup"
        )

    def test_break_slot_has_no_startup_id(self, coach_with_break):
        """A break slot must have Startup_id of None."""
        coaches, startups, feedbacks = coach_with_break
        result = assign_startups_to_coaches(coaches, startups, feedbacks)

        assignments = result["Coach Bob"]["Assignments"]
        break_assignments = [a for a in assignments if a["Slot"] == "Break"]

        assert break_assignments[0]["Startup_id"] is None, (
            "Break slot must have Startup_id of None"
        )

    def test_non_break_slots_filled_normally(self, coach_with_break):
        """Regular slots around a break should still be filled normally."""
        coaches, startups, feedbacks = coach_with_break
        result = assign_startups_to_coaches(coaches, startups, feedbacks)

        assignments = result["Coach Bob"]["Assignments"]
        regular_assignments = [
            a for a in assignments
            if a["Slot"] != "Break" and a["Startup_id"] is not None
        ]

        assert len(regular_assignments) > 0, (
            "Regular slots around a break should still be filled with startups"
        )


class TestNoRepeatMeetings:
    """Tests that verify a coach never meets the same startup twice."""

    def test_coach_does_not_meet_same_startup_twice(self, single_coach_single_startup):
        """When a coach has more slots than available startups, the extra
        slots must be empty — the same startup must never appear twice."""
        coaches, startups, feedbacks = single_coach_single_startup

        # Give the coach 3 slots but only 1 startup available
        coaches["Coach Alice"]["Availability"] = [
            {"Slot": "09:00 - 09:30", "Duration": "30 minutes"},
            {"Slot": "09:30 - 10:00", "Duration": "30 minutes"},
            {"Slot": "10:00 - 10:30", "Duration": "30 minutes"},
        ]

        result = assign_startups_to_coaches(coaches, startups, feedbacks)

        assignments = result["Coach Alice"]["Assignments"]
        startup_ids = [
            a["Startup_id"] for a in assignments
            if a["Startup_id"] is not None
        ]

        assert len(startup_ids) == len(set(startup_ids)), (
            f"Coach Alice met the same startup more than once: {startup_ids}"
        )

    def test_extra_slots_marked_empty_when_no_more_startups(
        self, single_coach_single_startup
    ):
        """When all available startups have been assigned, remaining
        slots must be marked as Empty."""
        coaches, startups, feedbacks = single_coach_single_startup

        coaches["Coach Alice"]["Availability"] = [
            {"Slot": "09:00 - 09:30", "Duration": "30 minutes"},
            {"Slot": "09:30 - 10:00", "Duration": "30 minutes"},
            {"Slot": "10:00 - 10:30", "Duration": "30 minutes"},
        ]

        result = assign_startups_to_coaches(coaches, startups, feedbacks)

        assignments = result["Coach Alice"]["Assignments"]
        empty_slots = [
            a for a in assignments
            if a["Startup_name"] == "Empty"
        ]

        assert len(empty_slots) == 2, (
            "With 3 slots and 1 startup, exactly 2 slots should be empty"
        )