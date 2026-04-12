from datetime import date as date_type
from backend.database import (
    Startups,
    CoachSlots,
    BannedToMeet,
    CoachAssignments
)
from backend.date_utils import parse_db_date



def run_matching_engine(today: date_type, compute_priority_fn):
    """
    Matching Engine (updated) - aligned with team logic:
    - Uses only future, non-break slots
    - Respects bans
    - Avoids double booking (coach & startup)
    - One startup per slot
    - Prioritizes startups via compute_priority_fn
    """

    # ---------------
    # 1. Load data
    # ---------------
    startups = Startups.query.all()

    slots = (
        CoachSlots.query
        .filter(CoachSlots.Date >= today)
        .filter(CoachSlots.IsBreak == False)
        .all()
    )

    bans = BannedToMeet.query.all()
    existing = CoachAssignments.query.all()

    # ----------------------
    # 2. Normalize slots
    # ----------------------
    available_slots = []
    for s in slots:
        slot_date = parse_db_date(s.Date)
        if not slot_date:
            continue

        available_slots.append({
            "SlotId": s.SlotId,
            "CoachId": s.CoachId,
            "Date": slot_date,
            "Slot": s.Slot,
            "Duration": s.Duration,
        })

    # Sort slots by date → coach → slot label
    available_slots.sort(key=lambda x: (x["Date"], x["CoachId"], x["Slot"]))

    # -------------------
    # 3. Build ban set
    # -------------------
    banned_pairs = set()
    for b in bans:
        d_from = parse_db_date(b.DateFrom)
        d_to = parse_db_date(b.DateTo)
        if not d_from or not d_to:
            continue
        if d_from <= today <= d_to:
            banned_pairs.add((b.StartupId, b.CoachId))

    # ------------------------------------------
    # 4. Build busy maps (avoid double booking)
    # ------------------------------------------
    coach_busy = set()    # (coach_id, date, slot)
    startup_busy = set()  # (startup_id, date, slot)

    for a in existing:
        a_date = parse_db_date(a.Date)
        if not a_date:
            continue
        coach_busy.add((a.CoachId, a_date, a.Slot))
        startup_busy.add((a.StartupId, a_date, a.Slot))

    # ----------------------------------
    # 5. Compute startup priorities
    # ----------------------------------
    startup_priorities = []
    for s in startups:
        score = compute_priority_fn(s.StartupId)
        startup_priorities.append({
            "StartupId": s.StartupId,
            "StartupName": s.StartupName,
            "priority": score,
        })

    # Lower score = higher priority
    startup_priorities.sort(key=lambda x: x["priority"])

    # -----------------------
    # 6. Main matching loop
    # -----------------------
    matches = []

    for s in startup_priorities:
        startup_id = s["StartupId"]
        startup_name = s["StartupName"]

        for idx, slot in enumerate(available_slots):
            coach_id = slot["CoachId"]
            slot_date = slot["Date"]
            slot_label = slot["Slot"]

            # Hard exclusion
            if (startup_id, coach_id) in banned_pairs:
                continue

            # Double booking checks
            if (coach_id, slot_date, slot_label) in coach_busy:
                continue
            if (startup_id, slot_date, slot_label) in startup_busy:
                continue

            # Assign
            matches.append({
                "StartupId": startup_id,
                "StartupName": startup_name,
                "CoachId": coach_id,
                "SlotId": slot["SlotId"],
                "Slot": slot_label,
                "Duration": slot["Duration"],
                "Date": slot_date,
            })

            # Mark busy
            coach_busy.add((coach_id, slot_date, slot_label))
            startup_busy.add((startup_id, slot_date, slot_label))

            # Consume slot (one startup per slot)
            del available_slots[idx]
            break

    return matches

