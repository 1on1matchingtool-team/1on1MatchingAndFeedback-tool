from backend.database.base import db

class DailyFeedback(db.Model):
    __tablename__ = 'daily_feedback'
    DailyFeedbackId = db.Column(db.Integer, primary_key=True)
    FeedbackText = db.Column(db.Text, nullable=True)
    Date = db.Column(db.Date, nullable=False)
    StartupId = db.Column(db.Integer, db.ForeignKey('startups.StartupId', ondelete="SET NULL"), nullable=True)
    CoachId = db.Column(db.Integer, db.ForeignKey('coaches.CoachId', ondelete="SET NULL"), nullable=True)

    # Relationships
    coach = db.relationship('Coaches', back_populates='daily_feedback', passive_deletes=True)
    startup = db.relationship('Startups', back_populates='daily_feedback', passive_deletes=True)
    feedback_history = db.relationship('FeedbackHistory', back_populates='daily_feedback')
