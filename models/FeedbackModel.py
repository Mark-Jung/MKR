from db import db

from models.basemodel import BaseModel
from utils.jsonable import JsonEncodedDict

class FeedbackModel(db.Model, BaseModel):
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    feedback_url= db.Column(db.String(255))
    feedback_duration= db.Column(db.Integer)
    transcription_url = db.Column(db.String(255))

    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))

    def __init__(self, feedback_duration, feedback_url, transcription_url, member_id):
        self.feedback_duration = feedback_duration
        self.feedback_url = feedback_url
        self.transcription_url = transcription_url
        self.member_id = member_id

    def json(self):
        return {
            "id": self.id,
            "date_created": self.date_created,
            "feedback_duration": self.feedback_duration,
            "feedback_url": self.feedback_url,
            "trancription_url": self.feedback_url,
            "member_id": self.member_id,
        }
    
    @classmethod
    def filter_by_member_id(cls, member_id):
        return cls.query.filter_by(member_id=member_id).all()
