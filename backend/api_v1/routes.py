from flask import Blueprint, jsonify
from datetime import datetime
from backend.matching_engine.engine import run_matching_engine
from backend.database.base import db
from backend.database import (
    BannedToMeet,
    CoachAssignments,
    CoachSlots,
    DailyFeedback,
    FeedbackHistory,
    Startups,
)

api_v1 = Blueprint("api_v1", __name__)


# Helper Function
def row_to_dict(row):
    return {col.name: getattr(row, col.name) for col in row.__table__.columns}

# -------------------------
# Trend and Priority Logic
# -------------------------

def compute_trend_score(startup_id):
    # Negative trend = higher priority, positive trend = lower priority.
    history = (
        FeedbackHistory.query
        .filter_by(StartupId=startup_id)
        .order_by(FeedbackHistory.DateFeedbackOriginal.asc())
        .all()
    )
    if len(history) < 2:
        return 0 # no trend

    prev = history[-2].StartupGrade
    last = history[-1].StartupGrade
    
    if last is None or prev is None:
        return 0
    return -1 if last < prev else 1

def compute_startup_priority(startup_id):
    # Compute a priority score for a startup. (Lower score = higher priority.)
    # Count past meetings
    past_meetings = CoachAssignments.query.filter_by(StartupId=startup_id).count()

    # Get latest grade from FeedbackHistory
    latest_history = (
        FeedbackHistory.query
        .filter_by(StartupId=startup_id)
        .order_by(FeedbackHistory.DateFeedbackOriginal.desc())
        .first()
    )

    latest_grade = latest_history.StartupGrade if latest_history else 3  # neutral default

    # Get average daily feedback grade (if numeric grades are stored)
    daily_avg = 3  # neutral default / placeholder

    # Trend score (negative = worse, so higher priority)
    trend_score = compute_trend_score(startup_id)

    # Priority formula (tunable)
    score = (latest_grade * 0.5) + (daily_avg * 0.2) + (past_meetings * 0.1) + (trend_score * 0.2)
    return score

# ---------------------------
# Business Logic Endpoints
# ---------------------------

@api_v1.route('/availability/<int:coach_id>', methods=['GET'])
def availability(coach_id):
    # Return all upcoming and non-break slots for a given coach
    try:
        today = datetime.today().date()
        slots = (
            CoachSlots.query
            .filter(CoachSlots.CoachId == coach_id)  # Query all slots for this coach that:
            .filter(CoachSlots.Date >= today)        # are on or after today
            .filter(CoachSlots.IsBreak == False)     # are not marked as break
            .all()
        )
        return jsonify([row_to_dict(s) for s in slots]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@api_v1.route('/feedback/<int:startup_id>', methods=['GET'])
def feedback(startup_id):
    # Return combined DailyFeedback + FeedbackHistory for a startup
    try:
        # Get all DailyFeedback for this startup
        daily = DailyFeedback.query.filter_by(StartupId=startup_id).all()
        # Get all FeedbackHistory for this startup
        history = FeedbackHistory.query.filter_by(StartupId=startup_id).all()
        # Build response
        response = {
            "startup_id": startup_id,
            "daily_feedback": [row_to_dict(d) for d in daily],
            "feedback_history": [row_to_dict(h) for h in history]
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Temporary debug
@api_v1.route('/debug/db', methods=['GET'])
def debug_db():
    from backend.database.base import db
    return {"db_path": str(db.engine.url)}

# ---------------------------------------
# Matching Algorithm Endpoint (Updated)
# ---------------------------------------

@api_v1.route('/match', methods=['POST'])
def match():
    try:
        today = datetime.today().date()

        # 1. Run the matching engine (current prototype)
        matches = run_matching_engine(today, compute_startup_priority)

        # 2. Save results to database
        saved = []
        for m in matches:
            new_assignment = CoachAssignments(
                StartupId=m["StartupId"],
                CoachId=m["CoachId"],
                SlotId=m["SlotId"],
                Slot=m["Slot"],
                Duration=m["Duration"],
                Date=m["Date"],
                StartupName=m["StartupName"]
            )
            db.session.add(new_assignment)
            saved.append(row_to_dict(new_assignment))

        # 3. Commit once
        db.session.commit()

        # 4. Return JSON
        return jsonify({"matches": saved}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
