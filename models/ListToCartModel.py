from db import db

from models.basemodel import BaseModel

class ListToCartModel(db.Model, BaseModel):
    __tablename__ = "ListToCart"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)

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
        self.in_store = in_store
        self.fam_id = fam_id
        self.adder = adder_name

        self.in_cart = False

    @classmethod
    def filter_by_fam_id(cls, fam_id):
        cls.query.filter_by(fam_id=fam_id).all()
    
    @classmethod
    def get_fam_list(cls, fam_id):
        cls.query.filter(fam_id==fam_id, in_cart==False).all()

    @classmethod
    def get_fam_cart(cls, fam_id):
        cls.query.filter(fam_id==fam_id, in_cart==True).all()
