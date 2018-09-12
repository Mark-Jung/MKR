from db import db

from models.basemodel import BaseModel
from utils.jsonable import JsonEncodedDict

class VerificationModel(db.Model, BaseModel):
    __tablename__ = "verification"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)

    value = db.Column(db.String(255))

    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))

    def __init__(self, value, member_id):
        self.value = value
        self.member_id = member_id

    def json(self):
        return {
            "id": self.id,
            "member_id": self.member_id,
            "value": self.value,
        }
    
    @classmethod
    def filter_by_member_id(cls, member_id):
        return cls.query.filter_by(member_id=member_id).all()

    @classmethod
    def find_by_value(cls, value):
        return cls.query.filter_by(value=value).first()