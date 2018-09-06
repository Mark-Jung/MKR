from db import db

from models.basemodel import BaseModel
from utils.jsonable import JsonEncodedDict

class CheckoutModel(db.Model, BaseModel):
    __tablename__ = "checkout"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)

    fam_id = db.Column(db.Integer, db.ForeignKey('family.id'))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    total = db.Column(db.Integer)

    def __init__(self, fam_id, first_name, last_name, total):
        self.fam_id = fam_id
        self.first_name = first_name
        self.last_name = last_name
        self.total = total

    def json(self):
        return {
            "fam_id": self.fam_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "total": self.total
        }

    @classmethod
    def filter_by_fam_id(cls, fam_id):
        return cls.query.filter_by(fam_id=fam_id).all()
