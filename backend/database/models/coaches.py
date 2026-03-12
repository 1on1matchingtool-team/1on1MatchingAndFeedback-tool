from backend.database.base import db
from sqlalchemy.dialects.sqlite import JSON

class Coaches(db.Model):
    __tablename__ = 'coaches'
    CoachId = db.Column(db.Integer, primary_key=True)
    # Required
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(60), nullable=False)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    # Optional contact methods
    Phone = db.Column(db.String(100), nullable=True)
    Chat = db.Column(db.String(100), nullable=True)
    # Profile information
    Bio = db.Column(db.Text, nullable=True)
    Expertise = db.Column(db.String(200), nullable=True)
    # Flexible list of social media links
    SocialMedia = db.Column(JSON, nullable=True)
    # Activity counters
    CoachingSessions = db.Column(db.Integer, nullable=False, default=0)
    BatchesCoached = db.Column(db.Integer, nullable=False, default=0)

    # Relationships
    slots = db.relationship('CoachSlots', back_populates='coach')
    feedback = db.relationship('FeedbackHistory', back_populates='coach')
    daily_feedback = db.relationship('DailyFeedback', back_populates='coach')
    assignments = db.relationship('CoachAssignments', back_populates='coach')
