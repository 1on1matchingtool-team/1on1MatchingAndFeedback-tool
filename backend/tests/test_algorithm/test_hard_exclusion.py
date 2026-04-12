# Tests that verify coach_grade=-1 startups are never assigned
# to that coach under any circumstances.

from backend.algo import assign_startups_to_coaches


class TestHardExclusions:
    """Tests that verify coach_grade=-1 startups are never assigned
    to that coach under any circumstances."""

    def test_hard_excluded_startup_never_assigned(self, coach_with_hard_exclusion):
        """A startup graded -1 by a coach must never appear in that
        coach's assignments, even if it is the only available startup."""
        coaches, startups, feedbacks = coach_with_hard_exclusion
        result = assign_startups_to_coaches(coaches, startups, feedbacks)

        assignments = result["Coach Alice"]["Assignments"]
        assigned_ids = [
            a["Startup_id"] for a in assignments
            if a["Startup_id"] is not None
        ]

        assert 0 not in assigned_ids, (
            "Startup 0 was hard-excluded by Coach Alice but still got assigned"
        )

    def test_hard_excluded_slot_marked_empty(self, coach_with_hard_exclusion):
        """When the only available startup is hard-excluded, the slot
        must be marked as Empty, not left unhandled or crashed."""
        coaches, startups, feedbacks = coach_with_hard_exclusion
        result = assign_startups_to_coaches(coaches, startups, feedbacks)

        assignments = result["Coach Alice"]["Assignments"]

        assert len(assignments) == 1, (
            "Coach Alice should have exactly one assignment entry"
        )
        assert assignments[0]["Startup_name"] == "Empty", (
            "Slot should be marked Empty when only startup is hard-excluded"
        )
        assert assignments[0]["Startup_id"] is None, (
            "Empty slot must have Startup_id of None"
        )

    def test_hard_excluded_startup_never_assigned_to_any_coach(
        self, all_coaches_exclude_startup
    ):
        """A startup hard-excluded by every coach must never appear
        in any coach's assignments anywhere in the result."""
        coaches, startups, feedbacks = all_coaches_exclude_startup
        result = assign_startups_to_coaches(coaches, startups, feedbacks)

        for coach_name, data in result.items():
            assigned_ids = [
                a["Startup_id"] for a in data["Assignments"]
                if a["Startup_id"] is not None
            ]
            assert 0 not in assigned_ids, (
                f"Startup 0 was hard-excluded by all coaches but was "
                f"assigned to {coach_name}"
            )

    def test_non_excluded_startup_still_assigned_normally(
        self, all_coaches_exclude_startup
    ):
        """When one startup is hard-excluded, other startups must still
        be assigned normally to fill available slots."""
        coaches, startups, feedbacks = all_coaches_exclude_startup
        result = assign_startups_to_coaches(coaches, startups, feedbacks)

        all_assigned_ids = [
            assignment["Startup_id"]
            for data in result.values()
            for assignment in data["Assignments"]
            if assignment["Startup_id"] is not None
        ]

        assert 1 in all_assigned_ids, (
            "Startup 1 was not excluded but was never assigned to any coach"
        )