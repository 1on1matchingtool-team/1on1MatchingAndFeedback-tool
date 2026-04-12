from backend.database.base import db

class Startups(db.Model):
    __tablename__ = 'startups'
    StartupId = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Core Identity
    StartupName = db.Column(db.String(100), nullable=False)
    Website = db.Column(db.String(255), nullable=False)

    # Status: alive / on-pause / dead
    Status = db.Column(db.String(20), nullable=False, default="alive")

    # Previous names (optional list of strings)
    PreviousNames = db.Column(db.JSON, nullable=False)

    # Members: list of objects with name, email, phone, role, level
    StartupMembers = db.Column(db.JSON, nullable=False)

    # Flexible social media links
    StartupSocialMedia = db.Column(db.JSON, nullable=True)

    # Optional description
    StartupDescription = db.Column(db.String(255), nullable=True)

    # Internal field for the tool
    MeetingsCount = db.Column(db.Integer, nullable=False, default=0)

    # Relationships
    feedback = db.relationship('FeedbackHistory', back_populates='startup', cascade="all, delete-orphan")
    daily_feedback = db.relationship('DailyFeedback', back_populates='startup', cascade="all, delete-orphan")
    assignments = db.relationship('CoachAssignments', back_populates='startup')
