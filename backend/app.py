from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import text
import logging
import os

# Initialize Flask app with a factory pattern for testing
def create_app(config=None):
    app = Flask(__name__)

    # ----------------------------
    # Database Configuration
    # ----------------------------
    # Default Configuration
    basedir = os.path.abspath(os.path.dirname(__file__))  # backend folder
    db_path = os.path.join(basedir, "instance", "sauna.db")

    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True  # Show SQL in logs

    # Override with test config if provided
    if config:
        app.config.update(config)
    
    # Initialize DB
    from backend.database.base import db
    db.init_app(app)

    # Import models so SQLAlchemy metadata includes them (even if PyCharm greys them out)
    from backend.database import (
        BannedToMeet,
        CoachAssignments,
        Coaches,
        CoachSlots,
        DailyFeedback,
        FeedbackHistory,
        Startups,
)

    # Register API blueprint(s)
    from backend.api_v1.routes import api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    # Enable CORS
    # CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    CORS(app)

    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    @app.before_request
    def log_request_info():
        logging.info(f"Request Headers: {request.headers}")

# --------------------------------------
# Health Check and Connectivity Routes
# --------------------------------------

    @app.route("/")  # Health check
    def home():
        return {"message": "API is running"}

    @app.route("/test-db")  # DB connectivity check
    def test_db():
        try:
            db.session.execute(text("SELECT 1"))  # Wrap raw SQL in text()
            return jsonify({"message": "Database connected successfully", "status": "ok"}), 200
        except Exception as e:
            return jsonify({"message": str(e), "status": "error"}), 500
        
    return app

# ----------------------------
# Initialize DB and Run App
# ----------------------------

if __name__ == "__main__":
    app = create_app()
    from backend.database.base import db
    with app.app_context():
        try:
            db.create_all()
            logging.info("✅ Tables created successfully.")
        except Exception as e:
            logging.error(f"❌ Error creating tables: {e}")
    app.run(debug=True)
