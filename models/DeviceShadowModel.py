from db import db
from datetime import datetime

from models.basemodel import BaseModel
from utils.jsonable import JsonEncodedDict

class DeviceShadowModel(db.Model, BaseModel):
    __tablename__ = "deviceshadow"

    device_id = db.Column(db.String(255), primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_updated = db.Column(db.DateTime)

    shadow_metadata = db.Column(JsonEncodedDict)
    alert_level = db.Column(db.Integer)
    auto_order_store = db.Column(db.String(200))
    container = db.Column(db.Integer)
    alias = db.Column(db.String(200))
    product_metadata = db.Column(JsonEncodedDict)

    fam_id = db.Column(db.Integer, db.ForeignKey('family.id'))

    def __init__(self, device_id):
        self.device_id = device_id
        self.date_created = datetime.now()
        self.date_updated = datetime.now()
        self.shadow_metadata = {}
        self.alert_level = 0
        self.container = 0
        self.alias = ""
        self.product_metadata = {}


    def json(self):
        return {
                "device_id": self.device_id,
                "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
                "date_updated": self.date_updated.strftime("%Y-%m-%d %H:%M:%S"),
                "shadow_metadata": self.shadow_metadata,
                "alert_level": self.alert_level,
                "container": self.container,
                "alias": self.alias,
                "auto_order_store": self.auto_order_store,
                "product_metadata": self.product_metadata,
                }

    @classmethod
    def find_by_device_id(cls, device_id):
        return cls.query.filter_by(device_id=device_id).first()

    @classmethod
    def filter_by_fam_id(cls, fam_id):
        return cls.query.filter_by(fam_id=fam_id).all()

