# Tests that verify a startup cannot be in two places at the same time.
# This is a critical constraint to ensure the integrity of the schedule.
# KNOWN GAP:
# More sophisticated double booking scenarios (e.g. 50 coaches competing
# for 20 startups with many overlapping slots) require access to
# global_taken_slots.
# Flagged as future improvement.

from backend.algo import assign_startups_to_coaches


class TestNoDoubleBooking:
    """Tests that verify a startup cannot be in two places at the same time."""

    def test_one_startup_cannot_be_in_two_places_same_slot(
        self, two_coaches_same_slots
    ):
        """When two coaches share the same time slot and only one startup
        is available, that startup can only be assigned to one of them."""
        coaches, startups, feedbacks = two_coaches_same_slots
        result = assign_startups_to_coaches(coaches, startups, feedbacks)

        slot = "09:00 - 09:30"
        startup_id = 0

        coaches_with_startup_in_slot = [
            coach_name
            for coach_name, data in result.items()
            for assignment in data["Assignments"]
            if assignment["Slot"] == slot
            and assignment["Startup_id"] == startup_id
        ]

        assert len(coaches_with_startup_in_slot) <= 1, (
            f"Startup {startup_id} was assigned to multiple coaches "
            f"at the same time slot {slot}: {coaches_with_startup_in_slot}"
        )

    def test_one_startup_one_slot_other_coach_gets_empty(
        self, two_coaches_same_slots
    ):
        """When only one startup is available for a shared slot,
        the coach that does not get the startup must have an empty slot."""
        coaches, startups, feedbacks = two_coaches_same_slots
        result = assign_startups_to_coaches(coaches, startups, feedbacks)

        slot = "09:00 - 09:30"
        startup_id = 0

        slot_outcomes = {}
        for coach_name, data in result.items():
            for assignment in data["Assignments"]:
                if assignment["Slot"] == slot:
                    slot_outcomes[coach_name] = assignment["Startup_id"]

        assigned_count = sum(
            1 for sid in slot_outcomes.values() if sid == startup_id
        )
        empty_count = sum(
            1 for sid in slot_outcomes.values() if sid is None
        )

        assert assigned_count == 1, (
            "Exactly one coach should get the startup"
        )
        assert empty_count == 1, (
            "The other coach should have an empty slot"
        )

    def test_no_startup_appears_in_same_slot_twice_across_all_coaches(
        self, two_coaches_same_slots
    ):
        """Across all coaches and all slots, no startup should appear
        in the same time slot more than once."""
        coaches, startups, feedbacks = two_coaches_same_slots
        result = assign_startups_to_coaches(coaches, startups, feedbacks)

        slot_map = {}
        for coach_name, data in result.items():
            for assignment in data["Assignments"]:
                startup_id = assignment["Startup_id"]
                if startup_id is None:
                    continue
                key = (startup_id, assignment["Slot"])
                slot_map.setdefault(key, []).append(coach_name)

        violations = {
            key: coaches_list
            for key, coaches_list in slot_map.items()
            if len(coaches_list) > 1
        }

        assert len(violations) == 0, (
            f"Double booking detected — startup appeared in same slot "
            f"for multiple coaches: {violations}"
        )

    def test_high_priority_startups_not_double_booked(
        self, two_coaches_high_priority_double_booking
    ):
        """Two coaches competing for two priority 1 startups in the same slot."""

        coaches, startups, feedbacks = two_coaches_high_priority_double_booking
        result = assign_startups_to_coaches(coaches, startups, feedbacks)
 
        slot = "09:00 - 09:30"
 
        # Find which startup each coach got in the shared slot
        slot_assignments = {}
        for coach_name, data in result.items():
            for assignment in data["Assignments"]:
                if assignment["Slot"] == slot:
                    slot_assignments[coach_name] = assignment["Startup_id"]
 
        # Both coaches should have a startup assigned
        assert slot_assignments.get("Coach Alice") is not None, (
            "Coach Alice should have a startup assigned in slot 09:00 - 09:30"
        )
        assert slot_assignments.get("Coach Bob") is not None, (
            "Coach Bob should have a startup assigned in slot 09:00 - 09:30"
        )
 
        # Each coach must have gotten a DIFFERENT startup
        assert slot_assignments["Coach Alice"] != slot_assignments["Coach Bob"], (
            f"Both coaches got the same startup "
            f"(id={slot_assignments['Coach Alice']}) "
            f"in the same slot — double booking detected"
        )