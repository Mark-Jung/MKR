from db import db
from datetime import datetime

from models.basemodel import BaseModel
from utils.jsonable import JsonEncodedDict

class FamilyModel(db.Model, BaseModel):
    __tablename__ = "family"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)

    address_line1 = db.Column(db.String(255))
    address_line2 = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(10))
    zip_code = db.Column(db.Integer)

    name = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(255))

    def __init__(self, address_line1, address_line2, city, state, zip_code, name, phone, email):
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.name = name
        self.phone = phone
        self.email = email

    def json(self):
        return {
            "address_line1": self.address_line1,
            "address_line2": self.address_line2,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_phone(cls, phone):
        return cls.query.filter_by(phone=phone).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(phone=phone).first()
