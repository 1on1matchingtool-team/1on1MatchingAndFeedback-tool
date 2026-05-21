from flask import request, jsonify
from backend.database.base import db
from backend.database import BannedToMeet
from backend.validation.banned_validation import validate_banned_to_meet
from backend.date_utils import parse_date, parse_db_date
from .routes import api_v1, row_to_dict

@api_v1.route("/banned_to_meet/all", methods=["GET"])
def get_all_banned_to_meet():
    try:
        rows = BannedToMeet.query.all()
        return jsonify([row_to_dict(r) for r in rows]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@api_v1.route("/banned_to_meet", methods=["GET"])
def get_banned_to_meet():
    try:
        coach_id = request.args.get("coachId", type=int)
        startup_id = request.args.get("startupId", type=int)
        active_only = request.args.get("activeOnly", "false").lower() == "true"

        query = BannedToMeet.query

        # Filter by coach
        if coach_id:
            query = query.filter_by(CoachId=coach_id)

        # Filter by startup
        if startup_id:
            query = query.filter_by(StartupId=startup_id)

        rows = query.all()

        # Filter active bans (DateTo is null or DateTo >= today)
        if active_only:
            today = parse_date("today")
            rows = [
                r for r in rows
                if r.DateTo is None or parse_db_date(r.DateTo) >= today
            ]

        return jsonify([row_to_dict(r) for r in rows]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@api_v1.route("/banned_to_meet/<int:id>", methods=["GET"])
def get_banned_to_meet_by_id(id):
    try:
        row = BannedToMeet.query.get(id)
        if not row:
            return jsonify({"error": "Not found"}), 404
        return jsonify(row_to_dict(row)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@api_v1.route("/banned_to_meet", methods=["POST"])
def add_banned_to_meet():
    data = request.json or {}
    validate_banned_to_meet(data)
    try:
        new_row = BannedToMeet(
            StartupId=data.get("StartupId"),
            CoachId=data.get("CoachId"),
            DateFrom=parse_date(data.get("DateFrom")),
            DateTo=parse_date(data.get("DateTo")),
            Reason=data.get("Reason"),
        )
        db.session.add(new_row)
        db.session.commit()
        return jsonify({"message": "BannedToMeet created", "id": new_row.RestrictionId}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@api_v1.route("/banned_to_meet/<int:id>", methods=["PATCH"])
def update_banned_to_meet(id):
    try:
        row = BannedToMeet.query.get(id)
        if not row:
            return jsonify({"error": "Not found"}), 404

        data = request.json or {}
        existing = row_to_dict(row)
        merged = {**existing, **data}
        validate_banned_to_meet(merged)

        for key, value in data.items():
            if key in ("DateFrom", "DateTo"):
                value = parse_date(value)
            if hasattr(row, key):
                setattr(row, key, value)

        db.session.commit()
        return jsonify({"message": "BannedToMeet updated"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@api_v1.route("/banned_to_meet/<int:id>", methods=["DELETE"])
def delete_banned_to_meet(id):
    try:
        row = BannedToMeet.query.get(id)
        if not row:
            return jsonify({"error": "Not found"}), 404

        db.session.delete(row)
        db.session.commit()
        return jsonify({"message": "BannedToMeet deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400