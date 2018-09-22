from db import db

from models.basemodel import BaseModel
from utils.jsonable import JsonEncodedDict

class CheckoutModel(db.Model, BaseModel):
    __tablename__ = "checkout"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    total = db.Column(db.Integer)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))

    def __init__(self, total, member_id):
        self.total = total
        self.member_id = member_id

    def json(self):
        return {
            "total": self.total,
            "member_id": self.member_id
        }

    @classmethod
    def filter_by_member_id(cls, member_id):
        return cls.query.filter_by(member_id=member_id).all()
