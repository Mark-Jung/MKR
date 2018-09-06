from db import db

from models.basemodel import BaseModel
from utils.jsonable import JsonEncodedDict

class ProductModel(db.Model, BaseModel):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)

    store = db.Column(db.String(255))
    price = db.Column(db.Integer)
    url = db.Column(db.String(255))
    name = db.Column(db.String(255))

    checkout_id = db.Column(db.Integer, db.ForeignKey('checkout.id'))

    def __init__(self, store, price, url, name, checkout_id):
        self.store = store
        self.price = price
        self.url = url
        self.name = name
        self.checkout_id = checkout_id

    def json(self):
        return {
            "store": self.store,
            "price": self.price / 100,
            "url": self.url,
            "name": self.name,
            "checkout_id": self.checkout_id,
        }

    @classmethod
    def filter_by_checkout_id(cls, checkout_id):
        return cls.query.filter_by(checkout_id=checkout_id).all()
    
    @classmethod
    def filter_by_url(cls, url):
        return cls.query.filter_by(url=url).first()
