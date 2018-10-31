from db import db

from models.basemodel import BaseModel
from utils.jsonable import JsonEncodedDict
import datetime

class CheckoutModel(db.Model, BaseModel):
    __tablename__ = "checkout"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)

    total = db.Column(db.Integer)
    fam_id = db.Column(db.Integer, db.ForeignKey('family.id'))
    member_id = db.Column(db.Integer)

    def __init__(self, total, fam_id, member_id):
        self.total = total
        self.fam_id = fam_id
        self.member_id = member_id
        self.date_created = datetime.datetime.now()

    def json(self):
        return {
            "id": self.id,
            "total": self.total,
            "fam_id": self.fam_id,
            "member_id": self.member_id,
            "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
        }
    @classmethod
    def filter_by_fam_id(cls, fam_id):
        return cls.query.filter_by(fam_id=fam_id).all()

    @classmethod
    def filter_by_member_id(cls, member_id):
        return cls.query.filter_by(member_id=member_id).all()
