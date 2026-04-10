# backend/tests/algorithm/test_zero_meetings.py
# Tests that verify startups with zero meetings are always assigned
# before startups with existing meeting history.
#
# APPROACH:
# These tests use invariant testing — we never check which specific
# startup goes first within the zero-meetings group, only that ALL
# zero-meetings startups are assigned before ANY veteran startup.
# This makes tests deterministic despite random.shuffle() within buckets.

from backend.algo import assign_startups_to_coaches


class TestZeroMeetingsPriority:
    """Tests that verify zero-meetings startups are assigned first."""

    def test_zero_meetings_startup_assigned_before_veteran(
        self, zero_meetings_vs_veterans
    ):
        """A startup with zero meetings must be assigned before any
        startup that has already had meetings."""
        coaches, startups, feedbacks = zero_meetings_vs_veterans
        result = assign_startups_to_coaches(coaches, startups, feedbacks)

        assignments = result["Coach Alice"]["Assignments"]
        assigned_ids = [
            a["Startup_id"] for a in assignments
            if a["Startup_id"] is not None
        ]

        # startup_id 2 is the only zero-meetings startup
        # startup_ids 0 and 1 are veterans
        if 2 in assigned_ids and (0 in assigned_ids or 1 in assigned_ids):
            zero_meetings_position = assigned_ids.index(2)
            veteran_positions = [
                assigned_ids.index(sid)
                for sid in [0, 1]
                if sid in assigned_ids
            ]
            assert all(
                zero_meetings_position < vet_pos
                for vet_pos in veteran_positions
            ), (
                f"Zero-meetings startup (id=2) was assigned after a veteran. "
                f"Assignment order: {assigned_ids}"
            )

    def test_zero_meetings_startup_is_assigned(self, zero_meetings_vs_veterans):
        """A zero-meetings startup must always be assigned — it should
        never be skipped in favour of veterans."""
        coaches, startups, feedbacks = zero_meetings_vs_veterans
        result = assign_startups_to_coaches(coaches, startups, feedbacks)

        all_assigned_ids = [
            assignment["Startup_id"]
            for data in result.values()
            for assignment in data["Assignments"]
            if assignment["Startup_id"] is not None
        ]

        assert 2 in all_assigned_ids, (
            "Zero-meetings startup (id=2) was never assigned "
            "despite slots being available"
        )

    def test_all_zero_meetings_assigned_before_veterans(
        self, zero_meetings_vs_veterans
    ):
        """When multiple zero-meetings startups exist, ALL of them must
        be assigned before any veteran startup gets a slot."""
        coaches, startups, feedbacks = zero_meetings_vs_veterans

        # Add a second zero-meetings startup to the fixture
        startups["Startup New 2"] = {"startup_id": 3, "meetings_count": 0}
        feedbacks["Coach Alice"]["Feedback_per_startup"] = []

        result = assign_startups_to_coaches(coaches, startups, feedbacks)

        assignments = result["Coach Alice"]["Assignments"]
        assigned_ids = [
            a["Startup_id"] for a in assignments
            if a["Startup_id"] is not None
        ]

        zero_meeting_ids = {2, 3}
        veteran_ids = {0, 1}

        assigned_zero = [sid for sid in assigned_ids if sid in zero_meeting_ids]
        assigned_veterans = [sid for sid in assigned_ids if sid in veteran_ids]

        if assigned_zero and assigned_veterans:
            last_zero_position = max(assigned_ids.index(sid) for sid in assigned_zero)
            first_veteran_position = min(assigned_ids.index(sid) for sid in assigned_veterans)

            assert last_zero_position < first_veteran_position, (
                f"A veteran startup was assigned before all zero-meetings "
                f"startups were placed. Assignment order: {assigned_ids}"
            )

    def test_meetings_count_incremented_after_zero_meetings_assigned(
        self, zero_meetings_vs_veterans
    ):
        """After a zero-meetings startup is assigned, its meetings_count
        must be incremented from 0 to 1."""
        coaches, startups, feedbacks = zero_meetings_vs_veterans

        # Confirm starting state
        assert startups["Startup New"]["meetings_count"] == 0

        assign_startups_to_coaches(coaches, startups, feedbacks)

        # meetings_count is updated in place on the startups dict
        assert startups["Startup New"]["meetings_count"] == 1, (
            "meetings_count for zero-meetings startup should be 1 "
            "after being assigned once"
        )