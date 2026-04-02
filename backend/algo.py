import json
import random
import os

# Check if running in test mode.
# When TEST_MODE=True, file loading is skipped entirely.
# Tests pass data directly to assign_startups_to_coaches().
TEST_MODE = os.getenv("TEST_MODE", "False") == "True"

if not TEST_MODE:
    try:
        with open('data/coachTimeWithBreaks.json', 'r') as f:
            coaches_json = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding coachTimeWithBreaks.json: {e}")
        coaches_json = {}
    except FileNotFoundError as e:
        print(f"coachTimeWithBreaks.json file not found: {e}")
        coaches_json = {}
    except Exception as e:
        print(f"Unexpected error loading coachTimeWithBreaks.json: {e}")
        coaches_json = {}

    try:
        with open('data/startups.json', 'r') as f:
            startups_json = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding startups.json: {e}")
        startups_json = {}
    except FileNotFoundError as e:
        print(f"startups.json file not found: {e}")
        startups_json = {}
    except Exception as e:
        print(f"Unexpected error loading startups.json: {e}")
        startups_json = {}

    try:
        with open('data/total_feedbacks.json', 'r') as f:
            feedbacks_json = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding total_feedbacks.json: {e}")
        feedbacks_json = {}
    except FileNotFoundError as e:
        print(f"total_feedbacks.json file not found: {e}")
        feedbacks_json = {}
    except Exception as e:
        print(f"Unexpected error loading total_feedbacks.json: {e}")
        feedbacks_json = {}

else:
    # Test mode — skip file loading entirely
    # Tests pass data directly to assign_startups_to_coaches()
    coaches_json = {}
    startups_json = {}
    feedbacks_json = {}

def assign_startups_to_coaches(coaches, startups, feedbacks):
    print("Starting assignment process...")
    assigned_startups = {}
    taken_slots = {coach_name: set() for coach_name in coaches}  # Track taken slots per coach
    global_taken_slots = {}  # Track global taken slots for each startup
    coach_meetings = {coach_name: set() for coach_name in coaches}  # Track meetings for each coach

    # Initialize coaches in the assigned_startups dictionary with empty lists
    for coach_name, coach_data in coaches.items():
        assigned_startups[coach_name] = {
            "Coach_id": coach_data["Coach_id"],
            "Assignments": []
        }

    # Create shadow-ban list based on feedback for each coach
    shadow_ban_startups_per_coach = {coach_name: set() for coach_name in coaches}
    for coach_name, coach_feedbacks in feedbacks.items():
        for feedback in coach_feedbacks["Feedback_per_startup"]:
            if feedback["Startup_grade"] is None:
                shadow_ban_startups_per_coach[coach_name].add(feedback["Startup_id"])
    for coach_name, shadow_ban in shadow_ban_startups_per_coach.items():
        print(f"Shadow-banned startups for {coach_name}: {list(shadow_ban)}")

    # Create three lists for assignment: startups with 0 meetings, startups_with_feedback, and shadow_ban startups
    startups_with_zero_meetings = [startup["startup_id"] for startup in startups.values() if startup["meetings_count"] == 0]
    print(f"Startups with zero meetings: {startups_with_zero_meetings}")

    # Categorize startups based on feedback for each coach
    startups_with_feedback_per_coach = {}
    for coach_name, coach_feedbacks in feedbacks.items():
        print(f"Processing feedback for coach {coach_name}...")
        print(f"Shadow-banned startups for coach {coach_name}: {list(shadow_ban_startups_per_coach[coach_name])}")
        feedback_list = []
        for feedback in coach_feedbacks["Feedback_per_startup"]:
            startup_id = feedback["Startup_id"]
            startup_grade = feedback["Startup_grade"]
            coach_grade = feedback["Coach_grade"]
            # Only add to feedback list if the startup is not in shadow ban for this coach
            if startup_id not in shadow_ban_startups_per_coach[coach_name]:
                feedback_list.append((startup_id, startup_grade, coach_grade))
                print(f"Added feedback: Startup ID = {startup_id}, Startup Grade = {startup_grade}, Coach Grade = {coach_grade}")

        # Sort startups with feedback based on priority
        feedback_list.sort(key=lambda x: (
            (x[1] == 1 and x[2] == 1),  # Priority 1: Startup_grade = 1, Coach_grade = 1
            (x[1] == 0 and x[2] == 1),  # Priority 2: Startup_grade = 0, Coach_grade = 1
            (x[1] == 1 and x[2] == 0),  # Priority 3: Startup_grade = 1, Coach_grade = 0
            (x[1] == 1 and x[2] is None),  # Priority 4: Startup_grade = 1, Coach_grade = None
            (x[1] == 0 and x[2] == 0),  # Priority 5: Startup_grade = 0, Coach_grade = 0
            (x[1] == 0 and x[2] is None),  # Priority 6: Startup_grade = 0, Coach_grade = None
            (x[1] == -1 and x[2] == 1),  # Priority 7: Startup_grade = -1, Coach_grade = 1
            (x[1] == -1 and x[2] == 0),  # Priority 8: Startup_grade = -1, Coach_grade = 0
            (x[1] == -1 and x[2] is None)  # Priority 9: Startup_grade = -1, Coach_grade = None
        ), reverse=True)

        # Separate sorted startups into priority arrays
        sorted_startups = [[] for _ in range(11)]
        for startup_id, startup_grade, coach_grade in feedback_list:
            if startup_grade == 1 and coach_grade == 1:
                sorted_startups[0].append(startup_id)
            elif startup_grade == 0 and coach_grade == 1:
                sorted_startups[1].append(startup_id)
            elif startup_grade == 1 and coach_grade == 0:
                sorted_startups[2].append(startup_id)
            elif startup_grade == 1 and coach_grade is None:
                sorted_startups[3].append(startup_id)
            elif startup_grade == 0 and coach_grade == 0:
                sorted_startups[4].append(startup_id)
            elif startup_grade == 0 and coach_grade is None:
                sorted_startups[6].append(startup_id)
            elif startup_grade == -1 and coach_grade == 1:
                sorted_startups[7].append(startup_id)
            elif startup_grade == -1 and coach_grade == 0:
                sorted_startups[8].append(startup_id)
            elif startup_grade == -1 and coach_grade is None:
                sorted_startups[9].append(startup_id)

        # Add shadow-banned startups for this coach
        for startup_id in shadow_ban_startups_per_coach[coach_name]:
            sorted_startups[10].append(startup_id)
        print(f"Shadow-banned startups added to priority 11 for coach {coach_name}: {sorted_startups[10]}")

        # Add startups that are not in Feedback_per_startup
        all_startup_ids = {startup_data["startup_id"] for startup_data in startups.values()}
        feedback_startup_ids = {startup_id for startup_id, _, _ in feedback_list}
        not_in_feedback_startups = list(all_startup_ids - feedback_startup_ids)

        # Remove shadow-banned and 0 meetings startups from not_in_feedback_startups
        not_in_feedback_startups = [startup for startup in not_in_feedback_startups if startup not in shadow_ban_startups_per_coach[coach_name] and startup not in startups_with_zero_meetings]
        sorted_startups[5].extend(not_in_feedback_startups)
        print(f"Startups not in feedback for coach {coach_name} (after removing shadow-banned and new): {not_in_feedback_startups}")

        # Print sorted startups by priority
        for idx, priority_array in enumerate(sorted_startups):
            print(f"Priority {idx + 1} startups for coach {coach_name}: {priority_array}")

        # Shuffle startups within each priority array if there are more than one
        for priority_array in sorted_startups:
            if len(priority_array) > 1:
                random.shuffle(priority_array)
                print(f"Shuffled startups in priority array: {priority_array}")

        # Flatten the list of sorted startups into a single list
        startups_with_feedback_per_coach[coach_name] = [startup for priority_array in sorted_startups for startup in priority_array]
        print(f"Flattened list of startups for coach {coach_name}: {startups_with_feedback_per_coach[coach_name]}")

    # Assign startups to coaches
    for coach_name, coach_data in coaches.items():
        print(f"Assigning startups to coach {coach_name}...")
        available_slots = coach_data.get("Availability", [])
        # Get a list of startups graded -1 by the coach to exclude them
        excluded_startups = {feedback["Startup_id"] for feedback in feedbacks.get(coach_name, {}).get("Feedback_per_startup", [])
                             if feedback["Coach_grade"] == -1}
        print(f"Excluded startups for coach {coach_name}: {excluded_startups}")

        startups_with_feedback = startups_with_feedback_per_coach.get(coach_name, [])
        print(f"Startups with zero meetings (shuffled): {startups_with_zero_meetings}\n")

        shadow_ban_startups_list = list(shadow_ban_startups_per_coach[coach_name])
        random.shuffle(shadow_ban_startups_list)
        print(f"Shadow-banned startups for coach {coach_name} (shuffled): {shadow_ban_startups_list}")

        for slot in available_slots:
            slot_time = slot.get("Slot")
            slot_duration = slot.get("Duration", "30 minutes")
            print(f"Checking slot {slot_time} for coach {coach_name}...")

            # Check if the slot is a break
            if slot_time == "Break":
                print(f"Slot {slot_time} is a break. Marking as empty.")
                assigned_startups[coach_name]["Assignments"].append({
                    "Startup_id": None,
                    "Startup_name": "Break",
                    "Slot": slot_time,
                    "Duration": slot_duration
                })
                continue  # Proceed to the next slot

            # Assign startups, checking for constraints
            assigned = False
            for assigned_startup_id in startups_with_zero_meetings:
                if (assigned_startup_id not in excluded_startups and
                        slot_time not in taken_slots[coach_name] and
                        slot_time not in global_taken_slots.get(assigned_startup_id, set()) and
                        assigned_startup_id not in coach_meetings[coach_name]):
                    print(f"Assigning startup {assigned_startup_id} to coach {coach_name}, slot {slot_time}")
                    assign_startup_to_slot(assigned_startup_id, coach_name, slot_time, slot_duration, assigned_startups, taken_slots, global_taken_slots, coach_meetings, startups)
                    assigned = True
                    break

            if not assigned:
                for assigned_startup_id in startups_with_feedback:
                    if (assigned_startup_id not in excluded_startups and
                            slot_time not in taken_slots[coach_name] and
                            slot_time not in global_taken_slots.get(assigned_startup_id, set()) and
                            assigned_startup_id not in coach_meetings[coach_name]):
                        print(f"Assigning startup {assigned_startup_id} (with feedback) to coach {coach_name}, slot {slot_time}")
                        assign_startup_to_slot(assigned_startup_id, coach_name, slot_time, slot_duration, assigned_startups, taken_slots, global_taken_slots, coach_meetings, startups)
                        assigned = True
                        break

            if not assigned:
                for assigned_startup_id in shadow_ban_startups_list:
                    if (assigned_startup_id not in excluded_startups and
                            slot_time not in taken_slots[coach_name] and
                            slot_time not in global_taken_slots.get(assigned_startup_id, set()) and
                            assigned_startup_id not in coach_meetings[coach_name]):
                        print(f"Assigning shadow-banned startup {assigned_startup_id} to coach {coach_name}, slot {slot_time}")
                        assign_startup_to_slot(assigned_startup_id, coach_name, slot_time, slot_duration, assigned_startups, taken_slots, global_taken_slots, coach_meetings, startups)
                        assigned = True
                        break

            if not assigned:
                print(f"No startup assigned to coach {coach_name} for slot {slot_time}. Marking as empty.")
                assigned_startups[coach_name]["Assignments"].append({
                    "Startup_id": None,
                    "Startup_name": "Empty",
                    "Slot": slot_time,
                    "Duration": slot_duration
                })

    print("Assignment process completed.")
    return assigned_startups


def assign_startup_to_slot(assigned_startup_id, coach_name, slot_time, slot_duration, assigned_startups, taken_slots, global_taken_slots, coach_meetings, startups):
    print(f"Assigning startup {assigned_startup_id} to coach {coach_name} for slot {slot_time} with duration {slot_duration}")
    # Assign the startup to the slot
    assigned_startups[coach_name]["Assignments"].append({
        "Startup_id": assigned_startup_id,
        "Startup_name": f"Startup {assigned_startup_id}",
        "Slot": slot_time,
        "Duration": slot_duration
    })

    # Update tracking
    taken_slots[coach_name].add(slot_time)
    global_taken_slots.setdefault(assigned_startup_id, set()).add(slot_time)
    coach_meetings[coach_name].add(assigned_startup_id)
    print(f"Updated tracking: taken_slots for coach {coach_name} = {taken_slots[coach_name]}, global_taken_slots for startup {assigned_startup_id} = {global_taken_slots[assigned_startup_id]}, coach_meetings for coach {coach_name} = {coach_meetings[coach_name]}\n")

    # Increment meetings_count for the assigned startup
    for startup in startups.values():
        if startup["startup_id"] == assigned_startup_id:
            startup["meetings_count"] += 1
            print(f"Incremented meetings_count for startup {assigned_startup_id}: {startup['meetings_count']}")
            break


# -------------------------------------------------------
# Only runs when executing algo.py directly, never on import
# -------------------------------------------------------

if __name__ == "__main__":
    assigned_startups = assign_startups_to_coaches(coaches_json, startups_json, feedbacks_json)

    assigned_startups_json = json.dumps(assigned_startups, indent=4)
    print(assigned_startups_json)

    with open('data/assigned_startups.json', 'w') as f:
        json.dump(assigned_startups, f, indent=4)

    with open('data/startups.json', 'w') as f:
        json.dump(startups_json, f, indent=4)