from flask import request, jsonify
from datetime import datetime
from backend.database.base import db
from backend.database import (Startups, DailyFeedback, FeedbackHistory)
from backend.validation.startup_validation import validate_startup
from .routes import api_v1, row_to_dict

import logging

@api_v1.route("/startups/all", methods=["GET"])
def get_startups():
    try:
        startups = Startups.query.all()
        return jsonify([row_to_dict(s) for s in startups]), 200
    except Exception as e:
        logging.error(f"Error fetching startups: {e}")
        return jsonify({"error": str(e)}), 400

@api_v1.route("/startups/<int:id>", methods=["GET"])
def get_startup_by_id(id):
    try:
        startup = Startups.query.get(id)
        if not startup:
            return jsonify({"error": "Startup not found"}), 404
        return jsonify(row_to_dict(startup)), 200
    except Exception as e:
        logging.error(f"Error fetching startup: {e}")
        return jsonify({"error": str(e)}), 400

@api_v1.route("/startups", methods=["POST"])
def add_startup():
    try:
        data = request.json or {}
        cleaned, warnings = validate_startup(data)

        new_startup = Startups(
            StartupName=cleaned.get("StartupName"),
            Website=cleaned.get("Website"),
            Status=cleaned.get("Status"),
            PreviousNames=cleaned.get("PreviousNames"),
            StartupMembers=cleaned.get("StartupMembers"),
            StartupSocialMedia=cleaned.get("StartupSocialMedia"),
            StartupDescription=cleaned.get("StartupDescription"),
            MeetingsCount=cleaned.get("MeetingsCount", 0),
        )
        db.session.add(new_startup)
        db.session.commit()

        response = {
            "message": "Startup added successfully",
            "startup": row_to_dict(new_startup)
        }
        if warnings:
            response["warnings"] = warnings

        return jsonify(response), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding startup: {e}")
        return jsonify({"error": str(e)}), 400

@api_v1.route("/startups/<int:id>", methods=["PATCH"])
def patch_startup(id):
    try:
        startup = Startups.query.get(id)
        if not startup:
            return jsonify({"error": "Not found"}), 404

        data = request.json or {}
        cleaned, warnings = validate_startup(data, is_patch=True)

        # Automatic StartupName history tracking
        if "StartupName" in cleaned:
            new_name = cleaned["StartupName"]
            old_name = startup.StartupName

            if new_name != old_name:
                # Ensure PreviousNames is a list
                if not startup.PreviousNames:
                    startup.PreviousNames = []

                # Convert old string entries to object format
                if startup.PreviousNames and isinstance(startup.PreviousNames[0], str):
                    startup.PreviousNames = [
                        {"name": n, "changedAt": None} for n in startup.PreviousNames
                    ]

                # Append older name and date
                startup.PreviousNames.append({
                    "name": old_name,
                    "changedAt": datetime.utcnow().strftime("%Y-%m-%d")
                })
                startup.StartupName = new_name

            data.pop("StartupName")

        # Generic update for all other fields
        for key, value in data.items():
            if hasattr(startup, key):
                setattr(startup, key, value)

        db.session.commit()
        response = {"message": "Startup updated"}
        if warnings:
            response["warnings"] = warnings

        return jsonify(response), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error updating startup: {e}")
        return jsonify({"error": str(e)}), 400

@api_v1.route("/startups/<int:id>", methods=["DELETE"])
def delete_startup(id):
    try:
        startup = Startups.query.get(id)
        if not startup:
            return jsonify({"error": "Startup not found"}), 404

        # Anonymize feedback (keep feedback, remove coach reference)
        DailyFeedback.query.filter_by(StartupId=id).update({"StartupId": None})
        FeedbackHistory.query.filter_by(StartupId=id).update({"StartupId": None})

        # Keep coach_assignments and banned_to_meet unchanged

        # Delete the startup
        db.session.delete(startup)
        db.session.commit()

        return jsonify({"message": "Startup deleted safely"}), 200


    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting startup: {e}")
        return jsonify({"error": str(e)}), 400