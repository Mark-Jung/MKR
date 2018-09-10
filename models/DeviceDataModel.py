from db import db
from datetime import datetime

from models.basemodel import BaseModel
from utils.jsonable import JsonEncodedDict

class DeviceDataModel(db.Model, BaseModel):
    __tablename__ = "devicedata"

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(255), db.ForeignKey('deviceshadow.device_id'))
    date_created = db.Column(db.DateTime)
    device_metadata = db.Column(JsonEncodedDict)

    def __init__(self, device_id, metadata):
        self.device_id = device_id
        self.device_metadata = metadata
        self.date_created = datetime.now()

    def json(self):
        return {
                "id": self.id,
                "device_id": self.device_id,
                "device_metadata": self.device_metadata,
                "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
                }

    @classmethod
    def filter_by_device_id(cls, device_id):
        return cls.query.filter_by(device_id=device_id).all()

