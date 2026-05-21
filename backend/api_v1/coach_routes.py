from flask import request, jsonify
from datetime import datetime
from backend.database.base import db
from backend.database import (Coaches, CoachSlots, CoachAssignments, DailyFeedback, FeedbackHistory)
from backend.validation.coach_validation import validate_coach
from backend.date_utils import parse_db_date
from backend.api_v1.routes import api_v1, row_to_dict
from sqlalchemy.exc import IntegrityError
import logging

@api_v1.route("/coaches/all", methods=["GET"])
def get_coaches():
    try:
        coaches = Coaches.query.all()
        return jsonify([row_to_dict(c) for c in coaches]), 200
    except Exception as e:
        logging.error(f"Error fetching coaches: {e}")
        return jsonify({"error": str(e)}), 400

@api_v1.route("/coaches/<int:id>", methods=["GET"])
def get_coach_by_id(id):
    try:
        coach = Coaches.query.get(id)
        if not coach:
            return jsonify({"error": "Coach not found"}), 404
        return jsonify(row_to_dict(coach)), 200
    except Exception as e:
        logging.error(f"Error fetching coach: {e}")
        return jsonify({"error": str(e)}), 400

@api_v1.route("/coaches", methods=["POST"])  # Add coach
def add_coach():
    try:
        data = request.json or {}
        cleaned, warnings = validate_coach(data)

        new_coach = Coaches(
            Title=cleaned.get("Title"),
            FirstName=cleaned.get("FirstName"),
            LastName=cleaned.get("LastName"),
            Email=cleaned.get("Email"),
            Phone=cleaned.get("Phone"),
            Chat=cleaned.get("Chat"),
            Bio=cleaned.get("Bio"),
            Expertise=cleaned.get("Expertise"),
            SocialMedia=cleaned.get("SocialMedia"),
            CoachingSessions=cleaned.get("CoachingSessions", 0),
            BatchesCoached=cleaned.get("BatchesCoached", 0)
        )
        try:
            db.session.add(new_coach)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Email already exists"}), 400

        response = {
            "message": "Coach added successfully",
            "coach": row_to_dict(new_coach)
        }
        if warnings:
            response["warnings"] = warnings

        return jsonify(response), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding coach: {e}")
        return jsonify({"error": str(e)}), 400

@api_v1.route("/coaches/<int:id>", methods=["PATCH"])
def patch_coach(id):
    try:
        coach = Coaches.query.get(id)
        if not coach:
            return jsonify({"error": "Coach not found"}), 404

        data = request.json or {}
        cleaned, warnings = validate_coach(data, is_patch=True)

        allowed_fields = {
            "Title", "FirstName", "LastName", "Email", "Phone", "Chat",
            "Bio", "Expertise", "SocialMedia",
            "CoachingSessions", "BatchesCoached"
        }

        for key, value in data.items():
            if key in allowed_fields:
                setattr(coach, key, value)

        db.session.commit()

        response = {"message": "Coach updated"}
        if warnings:
            response["warnings"] = warnings

        return jsonify(response), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error updating coach: {e}")
        return jsonify({"error": str(e)}), 400

@api_v1.route("/coaches/<int:id>", methods=["DELETE"])
def delete_coach(id):
    try:
        coach = Coaches.query.get(id)
        if not coach:
            return jsonify({"error": "Coach not found"}), 404
        now = datetime.utcnow().date()

        # Delete upcoming slots
        all_slots = CoachSlots.query.filter_by(CoachId=id).all()
        upcoming_slots = [
            s for s in all_slots
            if parse_db_date(s.Date) and parse_db_date(s.Date) >= now
        ]
        for slot in upcoming_slots:
            db.session.delete(slot)

        # Delete upcoming assignments
        all_assignments = CoachAssignments.query.filter_by(CoachId=id).all()
        upcoming_assignments = [
            a for a in all_assignments
            if parse_db_date(a.Date) and parse_db_date(a.Date) >= now
        ]
        for assignment in upcoming_assignments:
            db.session.delete(assignment)

        # Anonymize feedback (keep feedback, remove coach reference)
        DailyFeedback.query.filter_by(CoachId=id).update({"CoachId": None})
        FeedbackHistory.query.filter_by(CoachId=id).update({"CoachId": None})

        # Delete the coach
        db.session.delete(coach)
        db.session.commit()

        return jsonify({"message": "Coach deleted safely"}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting coach: {e}")
        return jsonify({"error": str(e)}), 400