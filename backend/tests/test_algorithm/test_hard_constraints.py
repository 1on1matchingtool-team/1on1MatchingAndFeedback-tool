from backend.algo import assign_startups_to_coaches


# ============================================================
# Breaks
# ============================================================

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


