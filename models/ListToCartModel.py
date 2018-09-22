from db import db

from models.basemodel import BaseModel

class ListToCartModel(db.Model, BaseModel):
    __tablename__ = "ListToCart"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    alias = db.Column(db.String(255))
    in_cart = db.Column(db.Boolean)
    in_store = db.Column(db.String(200))
    adder = db.Column(db.String(255))
    
    #product data
    item_name = db.Column(db.String(255))
    item_image = db.Column(db.String(255))
    item_price = db.Column(db.Integer)
    item_rating = db.Column(db.String(255))
    item_quantity = db.Column(db.Integer)

    fam_id = db.Column(db.Integer, db.ForeignKey('family.id'))

    def __init__(self, alias, in_store, fam_id, adder_name):
        self.alias = alias
        self.in_cart = False
        self.in_store = in_store
        self.adder = adder_name

        self.item_name = ""
        self.item_image = ""
        self.item_price = 0
        self.item_rating = ""
        self.item_quantity = 0

        self.fam_id = fam_id
    
    def json(self):
        return {
            "id": self.id,
            "alias": self.alias,
            "in_cart": self.in_cart,
            "in_store": self.in_store,
            "adder": self.adder,
            "item_name": self.item_name,
            "item_image": self.item_image,
            "item_price": self.item_price,
            "item_rating": self.item_rating,
            "item_quantity": self.item_quantity,
            "fam_id": self.fam_id,
        }

    @classmethod
    def filter_by_fam_id(cls, fam_id):
        return cls.query.filter_by(fam_id=fam_id).all()
    
    @classmethod
    def get_fam_list(cls, fam_id):
        return cls.query.filter(cls.fam_id==fam_id, cls.in_cart==False).all()

    @classmethod
    def get_fam_cart(cls, fam_id):
        return cls.query.filter(cls.fam_id==fam_id, cls.in_cart==True).all()
