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

# ============================================================
# Double Booking
# ============================================================
 
class TestNoDoubleBooking:
    """Tests that verify a startup cannot be in two places at the same time.
 
    KNOWN GAP:
    These tests cover the basic scenario — two coaches, one startup, same slot.
    This is reliable because with only one startup the algorithm must choose
    one coach and leave the other empty.
 
    Harder scenarios that are not yet covered:
    - Multiple startups at the same priority competing across many coaches
      (shuffle makes outcome non-deterministic at the coach assignment level)
    - Scale test with 50 coaches and 20 startups where many slots overlap
      (would require inspecting global_taken_slots directly, which is internal
      state not exposed by the return value)
 
    Future improvement: expose global_taken_slots in the return value or via
    a debug mode so tests can inspect it directly.
    """
 
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
 
        # Build map of (startup_id, slot) -> list of coaches
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

