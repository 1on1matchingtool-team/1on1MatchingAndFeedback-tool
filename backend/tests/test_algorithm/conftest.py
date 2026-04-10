import os
os.environ["TEST_MODE"] = "True"  # must be set before importing algorithm to ensure it uses test data from conftest.py instead of loading JSON files

import pytest


# ============================================================
# One coach, one startup, no feedback
# Used for basic assignment and hard constraint tests
# ============================================================

@pytest.fixture
def single_coach_single_startup():
    """One coach with two slots, one new startup, no feedback history."""
    coaches = {
        "Coach Alice": {
            "Coach_id": 0,
            "Needs_break": False,
            "Availability": [
                {"Slot": "09:00 - 09:30", "Duration": "30 minutes"},
                {"Slot": "09:30 - 10:00", "Duration": "30 minutes"},
            ]
        }
    }
    startups = {
        "Startup New": {
            "startup_id": 0,
            "meetings_count": 0
        }
    }
    feedbacks = {
        "Coach Alice": {
            "Coach_id": 0,
            "Feedback_per_startup": []
        }
    }
    return coaches, startups, feedbacks


@pytest.fixture
def coach_with_break():
    """One coach with a break slot.
    Used to verify breaks are never overwritten."""
    coaches = {
        "Coach Bob": {
            "Coach_id": 1,
            "Needs_break": True,
            "Availability": [
                {"Slot": "09:00 - 09:30", "Duration": "30 minutes"},
                {"Slot": "Break", "Duration": "Break"},
                {"Slot": "10:00 - 10:30", "Duration": "30 minutes"},
            ]
        }
    }
    startups = {
        "Startup A": {"startup_id": 0, "meetings_count": 0},
        "Startup B": {"startup_id": 1, "meetings_count": 0},
        "Startup C": {"startup_id": 2, "meetings_count": 0},
    }
    feedbacks = {
        "Coach Bob": {
            "Coach_id": 1,
            "Feedback_per_startup": []
        }
    }
    return coaches, startups, feedbacks


# ============================================================
# Zero meetings priority fixtures
# ============================================================

@pytest.fixture
def zero_meetings_vs_old_startups():
    """One coach, mix of new and old startups, no feedback.
    Used to verify zero-meetings startups are assigned first."""
    coaches = {
        "Coach Alice": {
            "Coach_id": 0,
            "Needs_break": False,
            "Availability": [
                {"Slot": "09:00 - 09:30", "Duration": "30 minutes"},
                {"Slot": "09:30 - 10:00", "Duration": "30 minutes"},
                {"Slot": "10:00 - 10:30", "Duration": "30 minutes"},
            ]
        }
    }
    startups = {
        "Startup Old A": {"startup_id": 0, "meetings_count": 5},
        "Startup Old B": {"startup_id": 1, "meetings_count": 3},
        "Startup New":  {"startup_id": 2, "meetings_count": 0},  # only new one
    }
    feedbacks = {
        "Coach Alice": {
            "Coach_id": 0,
            "Feedback_per_startup": []
        }
    }
    return coaches, startups, feedbacks


# ============================================================
# Hard exclusion fixtures
# ============================================================

@pytest.fixture
def coach_with_hard_exclusion():
    """One coach who has graded one startup -1.
    Used to verify hard excluded startups are never assigned."""
    coaches = {
        "Coach Alice": {
            "Coach_id": 0,
            "Needs_break": False,
            "Availability": [
                {"Slot": "09:00 - 09:30", "Duration": "30 minutes"},
            ]
        }
    }
    startups = {
        "Startup Excluded": {"startup_id": 0, "meetings_count": 3},
    }
    feedbacks = {
        "Coach Alice": {
            "Coach_id": 0,
            "Feedback_per_startup": [
                {
                    "Startup_id": 0,
                    "Startup_name": "Startup Excluded",
                    "Startup_grade": 0,
                    "Coach_grade": -1,      # hard exclusion
                    "Startup_text_feedback": "",
                    "Coach_text_feedback": ""
                }
            ]
        }
    }
    return coaches, startups, feedbacks


@pytest.fixture
def all_coaches_exclude_startup():
    """Multiple coaches all excluding the same startup with -1.
    Used to verify the startup is never assigned anywhere."""
    coaches = {
        "Coach Alice": {
            "Coach_id": 0,
            "Needs_break": False,
            "Availability": [
                {"Slot": "09:00 - 09:30", "Duration": "30 minutes"},
            ]
        },
        "Coach Bob": {
            "Coach_id": 1,
            "Needs_break": False,
            "Availability": [
                {"Slot": "09:00 - 09:30", "Duration": "30 minutes"},
            ]
        }
    }
    startups = {
        "Startup Excluded": {"startup_id": 0, "meetings_count": 3},
        "Startup Normal":   {"startup_id": 1, "meetings_count": 2},
    }
    feedbacks = {
        "Coach Alice": {
            "Coach_id": 0,
            "Feedback_per_startup": [
                {
                    "Startup_id": 0,
                    "Startup_name": "Startup Excluded",
                    "Startup_grade": 0,
                    "Coach_grade": -1,
                    "Startup_text_feedback": "",
                    "Coach_text_feedback": ""
                }
            ]
        },
        "Coach Bob": {
            "Coach_id": 1,
            "Feedback_per_startup": [
                {
                    "Startup_id": 0,
                    "Startup_name": "Startup Excluded",
                    "Startup_grade": 0,
                    "Coach_grade": -1,
                    "Startup_text_feedback": "",
                    "Coach_text_feedback": ""
                }
            ]
        }
    }
    return coaches, startups, feedbacks


# ============================================================
# No double booking fixtures
# ============================================================

@pytest.fixture
def two_coaches_same_slots():
    """Two coaches with overlapping time slots, one startup.
    Used to verify a startup cannot be in two places at the same time."""
    coaches = {
        "Coach Alice": {
            "Coach_id": 0,
            "Needs_break": False,
            "Availability": [
                {"Slot": "09:00 - 09:30", "Duration": "30 minutes"},
            ]
        },
        "Coach Bob": {
            "Coach_id": 1,
            "Needs_break": False,
            "Availability": [
                {"Slot": "09:00 - 09:30", "Duration": "30 minutes"},
            ]
        }
    }
    startups = {
        "Startup A": {"startup_id": 0, "meetings_count": 0},
    }
    feedbacks = {
        "Coach Alice": {"Coach_id": 0, "Feedback_per_startup": []},
        "Coach Bob":   {"Coach_id": 1, "Feedback_per_startup": []},
    }
    return coaches, startups, feedbacks

@pytest.fixture
def two_coaches_high_priority_double_booking():
    """Two coaches each with one slot at the same time, two startups
    both at priority 1 (startup=1, coach=1) for both coaches."""
    
    coaches = {
        "Coach Alice": {
            "Coach_id": 0,
            "Needs_break": False,
            "Availability": [
                {"Slot": "09:00 - 09:30", "Duration": "30 minutes"},
            ]
        },
        "Coach Bob": {
            "Coach_id": 1,
            "Needs_break": False,
            "Availability": [
                {"Slot": "09:00 - 09:30", "Duration": "30 minutes"},
            ]
        }
    }
    startups = {
        "Startup P1A": {"startup_id": 0, "meetings_count": 2},  # priority 1 for both coaches
        "Startup P1B": {"startup_id": 1, "meetings_count": 2},  # priority 1 for both coaches
    }
    feedbacks = {
        "Coach Alice": {
            "Coach_id": 0,
            "Feedback_per_startup": [
                {
                    "Startup_id": 0,
                    "Startup_name": "Startup P1A",
                    "Startup_grade": 1,
                    "Coach_grade": 1,   # priority 1
                    "Startup_text_feedback": "",
                    "Coach_text_feedback": ""
                },
                {
                    "Startup_id": 1,
                    "Startup_name": "Startup P1B",
                    "Startup_grade": 1,
                    "Coach_grade": 1,   # priority 1
                    "Startup_text_feedback": "",
                    "Coach_text_feedback": ""
                },
            ]
        },
        "Coach Bob": {
            "Coach_id": 1,
            "Feedback_per_startup": [
                {
                    "Startup_id": 0,
                    "Startup_name": "Startup P1A",
                    "Startup_grade": 1,
                    "Coach_grade": 1,   # priority 1
                    "Startup_text_feedback": "",
                    "Coach_text_feedback": ""
                },
                {
                    "Startup_id": 1,
                    "Startup_name": "Startup P1B",
                    "Startup_grade": 1,
                    "Coach_grade": 1,   # priority 1
                    "Startup_text_feedback": "",
                    "Coach_text_feedback": ""
                },
            ]
        }
    }
    return coaches, startups, feedbacks


# ============================================================
# Priority matrix fixtures
# ============================================================

@pytest.fixture
def priority_matrix_coach():
    """One coach with multiple slots, startups covering all 9 priority
    combinations. Used to test the feedback priority ordering."""
    coaches = {
        "Coach Alice": {
            "Coach_id": 0,
            "Needs_break": False,
            "Availability": [
                {"Slot": "09:00 - 09:30", "Duration": "30 minutes"},
                {"Slot": "09:30 - 10:00", "Duration": "30 minutes"},
                {"Slot": "10:00 - 10:30", "Duration": "30 minutes"},
                {"Slot": "10:30 - 11:00", "Duration": "30 minutes"},
                {"Slot": "11:00 - 11:30", "Duration": "30 minutes"},
                {"Slot": "11:30 - 12:00", "Duration": "30 minutes"},
                {"Slot": "12:00 - 12:30", "Duration": "30 minutes"},
                {"Slot": "12:30 - 13:00", "Duration": "30 minutes"},
                {"Slot": "13:00 - 13:30", "Duration": "30 minutes"},
            ]
        }
    }
    startups = {
        "Startup P1": {"startup_id": 1, "meetings_count": 2},  # priority 1: both +1
        "Startup P2": {"startup_id": 2, "meetings_count": 2},  # priority 2: startup 0, coach +1
        "Startup P3": {"startup_id": 3, "meetings_count": 2},  # priority 3: startup +1, coach 0
        "Startup P4": {"startup_id": 4, "meetings_count": 2},  # priority 4: startup +1, coach None
        "Startup P5": {"startup_id": 5, "meetings_count": 2},  # priority 5: startup 0, coach 0
        "Startup P6": {"startup_id": 6, "meetings_count": 2},  # priority 6: not in feedback
        "Startup P7": {"startup_id": 7, "meetings_count": 2},  # priority 7: startup -1, coach +1
        "Startup P8": {"startup_id": 8, "meetings_count": 2},  # priority 8: startup -1, coach 0
        "Startup P9": {"startup_id": 9, "meetings_count": 2},  # priority 9: startup -1, coach None
    }
    feedbacks = {
        "Coach Alice": {
            "Coach_id": 0,
            "Feedback_per_startup": [
                {
                    "Startup_id": 1,
                    "Startup_name": "Startup P1",
                    "Startup_grade": 1,
                    "Coach_grade": 1,
                    "Startup_text_feedback": "",
                    "Coach_text_feedback": ""
                },
                {
                    "Startup_id": 2,
                    "Startup_name": "Startup P2",
                    "Startup_grade": 0,
                    "Coach_grade": 1,
                    "Startup_text_feedback": "",
                    "Coach_text_feedback": ""
                },
                {
                    "Startup_id": 3,
                    "Startup_name": "Startup P3",
                    "Startup_grade": 1,
                    "Coach_grade": 0,
                    "Startup_text_feedback": "",
                    "Coach_text_feedback": ""
                },
                {
                    "Startup_id": 4,
                    "Startup_name": "Startup P4",
                    "Startup_grade": 1,
                    "Coach_grade": None,
                    "Startup_text_feedback": "",
                    "Coach_text_feedback": ""
                },
                {
                    "Startup_id": 5,
                    "Startup_name": "Startup P5",
                    "Startup_grade": 0,
                    "Coach_grade": 0,
                    "Startup_text_feedback": "",
                    "Coach_text_feedback": ""
                },
                # Startup P6 intentionally not in feedback — priority 6
                {
                    "Startup_id": 7,
                    "Startup_name": "Startup P7",
                    "Startup_grade": -1,
                    "Coach_grade": 1,
                    "Startup_text_feedback": "",
                    "Coach_text_feedback": ""
                },
                {
                    "Startup_id": 8,
                    "Startup_name": "Startup P8",
                    "Startup_grade": -1,
                    "Coach_grade": 0,
                    "Startup_text_feedback": "",
                    "Coach_text_feedback": ""
                },
                {
                    "Startup_id": 9,
                    "Startup_name": "Startup P9",
                    "Startup_grade": -1,
                    "Coach_grade": None,
                    "Startup_text_feedback": "",
                    "Coach_text_feedback": ""
                },
            ]
        }
    }
    return coaches, startups, feedbacks


# ============================================================
# Scale fixtures
# ============================================================

@pytest.fixture
def max_scale():
    """20 startups and 50 coaches at maximum session scale.
    Used to verify the algorithm completes without errors at full load."""

    coaches = {}
    for i in range(50):
        coaches[f"Coach {i}"] = {
            "Coach_id": i,
            "Needs_break": i % 2 == 0,  # every other coach has a break
            "Availability": [
                {"Slot": "09:00 - 09:30", "Duration": "30 minutes"},
                {"Slot": "09:30 - 10:00", "Duration": "30 minutes"},
                {"Slot": "10:00 - 10:30", "Duration": "30 minutes"},
            ] + (
                [{"Slot": "Break", "Duration": "Break"}] if i % 2 == 0 else []
            ) + [
                {"Slot": "11:00 - 11:30", "Duration": "30 minutes"},
                {"Slot": "11:30 - 12:00", "Duration": "30 minutes"},
            ]
        }

    startups = {}
    for i in range(20):
        startups[f"Startup {i}"] = {
            "startup_id": i,
            "meetings_count": 0 if i < 5 else i  # first 5 are new startups
        }

    feedbacks = {}
    for i in range(50):
        feedbacks[f"Coach {i}"] = {
            "Coach_id": i,
            "Feedback_per_startup": []
        }

    return coaches, startups, feedbacks