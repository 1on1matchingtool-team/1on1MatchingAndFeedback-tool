# Tests that verify the feedback priority ordering is respected.
#
# APPROACH:
# Each test checks the boundary between two consecutive priority levels.
# The exact order within the same priority level is never tested since
# random.shuffle() makes that non-deterministic by design.
# ALL startups from a higher priority level should always
# appear before ANY startup from a lower priority level.
#
# Priority levels:
# P1 — startup=1,  coach=1
# P2 — startup=0,  coach=1
# P3 — startup=1,  coach=0
# P4 — startup=1,  coach=None
# P5 — startup=0,  coach=0
# P6 — not in feedback at all
# P7 — startup=-1, coach=1
# P8 — startup=-1, coach=0
# P9 — startup=-1, coach=None

from backend.algo import assign_startups_to_coaches


def get_assigned_position(assignments, startup_id):
    """Helper — returns the position of a startup in the assignment list.
    Returns None if the startup was not assigned."""
    for i, assignment in enumerate(assignments):
        if assignment["Startup_id"] == startup_id:
            return i
    return None


class TestPriorityMatrix:
    """Tests that verify the 9-level priority matrix is respected."""

    def test_p1_before_p2(self, priority_matrix_coach):
        """Priority 1 (startup=1, coach=1) must be assigned
        before Priority 2 (startup=0, coach=1)."""
        coaches, startups, feedbacks = priority_matrix_coach
        result = assign_startups_to_coaches(coaches, startups, feedbacks)
        assignments = result["Coach Alice"]["Assignments"]

        p1_pos = get_assigned_position(assignments, 1)
        p2_pos = get_assigned_position(assignments, 2)

        assert p1_pos is not None, "Priority 1 startup was not assigned"
        assert p2_pos is not None, "Priority 2 startup was not assigned"
        assert p1_pos < p2_pos, (
            f"Priority 1 startup (pos={p1_pos}) should be assigned "
            f"before Priority 2 startup (pos={p2_pos})"
        )

    def test_p2_before_p3(self, priority_matrix_coach):
        """Priority 2 (startup=0, coach=1) must be assigned
        before Priority 3 (startup=1, coach=0)."""
        coaches, startups, feedbacks = priority_matrix_coach
        result = assign_startups_to_coaches(coaches, startups, feedbacks)
        assignments = result["Coach Alice"]["Assignments"]

        p2_pos = get_assigned_position(assignments, 2)
        p3_pos = get_assigned_position(assignments, 3)

        assert p2_pos is not None, "Priority 2 startup was not assigned"
        assert p3_pos is not None, "Priority 3 startup was not assigned"
        assert p2_pos < p3_pos, (
            f"Priority 2 startup (pos={p2_pos}) should be assigned "
            f"before Priority 3 startup (pos={p3_pos})"
        )

    def test_p3_before_p4(self, priority_matrix_coach):
        """Priority 3 (startup=1, coach=0) must be assigned
        before Priority 4 (startup=1, coach=None)."""
        coaches, startups, feedbacks = priority_matrix_coach
        result = assign_startups_to_coaches(coaches, startups, feedbacks)
        assignments = result["Coach Alice"]["Assignments"]

        p3_pos = get_assigned_position(assignments, 3)
        p4_pos = get_assigned_position(assignments, 4)

        assert p3_pos is not None, "Priority 3 startup was not assigned"
        assert p4_pos is not None, "Priority 4 startup was not assigned"
        assert p3_pos < p4_pos, (
            f"Priority 3 startup (pos={p3_pos}) should be assigned "
            f"before Priority 4 startup (pos={p4_pos})"
        )

    def test_p4_before_p5(self, priority_matrix_coach):
        """Priority 4 (startup=1, coach=None) must be assigned
        before Priority 5 (startup=0, coach=0)."""
        coaches, startups, feedbacks = priority_matrix_coach
        result = assign_startups_to_coaches(coaches, startups, feedbacks)
        assignments = result["Coach Alice"]["Assignments"]

        p4_pos = get_assigned_position(assignments, 4)
        p5_pos = get_assigned_position(assignments, 5)

        assert p4_pos is not None, "Priority 4 startup was not assigned"
        assert p5_pos is not None, "Priority 5 startup was not assigned"
        assert p4_pos < p5_pos, (
            f"Priority 4 startup (pos={p4_pos}) should be assigned "
            f"before Priority 5 startup (pos={p5_pos})"
        )

    def test_p5_before_p6(self, priority_matrix_coach):
        """Priority 5 (startup=0, coach=0) must be assigned
        before Priority 6 (not in feedback at all)."""
        coaches, startups, feedbacks = priority_matrix_coach
        result = assign_startups_to_coaches(coaches, startups, feedbacks)
        assignments = result["Coach Alice"]["Assignments"]

        p5_pos = get_assigned_position(assignments, 5)
        p6_pos = get_assigned_position(assignments, 6)

        assert p5_pos is not None, "Priority 5 startup was not assigned"
        assert p6_pos is not None, "Priority 6 startup was not assigned"
        assert p5_pos < p6_pos, (
            f"Priority 5 startup (pos={p5_pos}) should be assigned "
            f"before Priority 6 startup (pos={p6_pos})"
        )

    def test_p6_before_p7(self, priority_matrix_coach):
        """Priority 6 (not in feedback) must be assigned
        before Priority 7 (startup=-1, coach=1)."""
        coaches, startups, feedbacks = priority_matrix_coach
        result = assign_startups_to_coaches(coaches, startups, feedbacks)
        assignments = result["Coach Alice"]["Assignments"]

        p6_pos = get_assigned_position(assignments, 6)
        p7_pos = get_assigned_position(assignments, 7)

        assert p6_pos is not None, "Priority 6 startup was not assigned"
        assert p7_pos is not None, "Priority 7 startup was not assigned"
        assert p6_pos < p7_pos, (
            f"Priority 6 startup (pos={p6_pos}) should be assigned "
            f"before Priority 7 startup (pos={p7_pos})"
        )

    def test_p7_before_p8(self, priority_matrix_coach):
        """Priority 7 (startup=-1, coach=1) must be assigned
        before Priority 8 (startup=-1, coach=0)."""
        coaches, startups, feedbacks = priority_matrix_coach
        result = assign_startups_to_coaches(coaches, startups, feedbacks)
        assignments = result["Coach Alice"]["Assignments"]

        p7_pos = get_assigned_position(assignments, 7)
        p8_pos = get_assigned_position(assignments, 8)

        assert p7_pos is not None, "Priority 7 startup was not assigned"
        assert p8_pos is not None, "Priority 8 startup was not assigned"
        assert p7_pos < p8_pos, (
            f"Priority 7 startup (pos={p7_pos}) should be assigned "
            f"before Priority 8 startup (pos={p8_pos})"
        )

    def test_p8_before_p9(self, priority_matrix_coach):
        """Priority 8 (startup=-1, coach=0) must be assigned
        before Priority 9 (startup=-1, coach=None)."""
        coaches, startups, feedbacks = priority_matrix_coach
        result = assign_startups_to_coaches(coaches, startups, feedbacks)
        assignments = result["Coach Alice"]["Assignments"]

        p8_pos = get_assigned_position(assignments, 8)
        p9_pos = get_assigned_position(assignments, 9)

        assert p8_pos is not None, "Priority 8 startup was not assigned"
        assert p9_pos is not None, "Priority 9 startup was not assigned"
        assert p8_pos < p9_pos, (
            f"Priority 8 startup (pos={p8_pos}) should be assigned "
            f"before Priority 9 startup (pos={p9_pos})"
        )

    def test_p1_before_p9(self, priority_matrix_coach):
        """End to end — Priority 1 must always be assigned
        before Priority 9, regardless of what happens in between."""
        coaches, startups, feedbacks = priority_matrix_coach
        result = assign_startups_to_coaches(coaches, startups, feedbacks)
        assignments = result["Coach Alice"]["Assignments"]

        p1_pos = get_assigned_position(assignments, 1)
        p9_pos = get_assigned_position(assignments, 9)

        assert p1_pos is not None, "Priority 1 startup was not assigned"
        assert p9_pos is not None, "Priority 9 startup was not assigned"
        assert p1_pos < p9_pos, (
            f"Priority 1 startup (pos={p1_pos}) should be assigned "
            f"before Priority 9 startup (pos={p9_pos})"
        )

    def test_all_priorities_assigned(self, priority_matrix_coach):
        """All 9 priority startups must be assigned — none should be skipped."""
        coaches, startups, feedbacks = priority_matrix_coach
        result = assign_startups_to_coaches(coaches, startups, feedbacks)
        assignments = result["Coach Alice"]["Assignments"]

        assigned_ids = [
            a["Startup_id"] for a in assignments
            if a["Startup_id"] is not None
        ]

        for priority_id in range(1, 10):
            assert priority_id in assigned_ids, (
                f"Priority {priority_id} startup (id={priority_id}) "
                f"was never assigned"
            )