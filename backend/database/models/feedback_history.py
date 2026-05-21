from backend.database.base import db

class FeedbackHistory(db.Model):
    __tablename__ = 'feedback_history'
    FeedbackHistoryId = db.Column(db.Integer, primary_key=True)
    StartupName = db.Column(db.String(100), nullable=False)
    DateFeedbackOriginal = db.Column(db.Date, nullable=False)
    StartupGrade = db.Column(db.Integer, nullable=False)
    CoachGrade = db.Column(db.Integer, nullable=False)
    StartupTextFeedback = db.Column(db.Text, nullable=True)
    CoachTextFeedback = db.Column(db.Text, nullable=True)
    UpdatedStartupGrade = db.Column(db.Integer, nullable=True)
    DateUpdatedStartupGrade = db.Column(db.Date, nullable=True)
    DailyFeedbackId = db.Column(db.Integer, db.ForeignKey('daily_feedback.DailyFeedbackId'), nullable=False)
    StartupId = db.Column(db.Integer, db.ForeignKey('startups.StartupId', ondelete="SET NULL"), nullable=True)
    CoachId = db.Column(db.Integer, db.ForeignKey('coaches.CoachId', ondelete="SET NULL"), nullable=True)

    # Relationships
    coach = db.relationship('Coaches', back_populates='feedback', passive_deletes=True)
    startup = db.relationship('Startups', back_populates='feedback', passive_deletes=True)
    daily_feedback = db.relationship('DailyFeedback', back_populates='feedback_history')
