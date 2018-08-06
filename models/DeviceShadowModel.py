from db import db
from models.basemodel import BaseModel
from utils.jsonable import JsonEncodedDict

class DeviceShadowModel(db.Model, BaseModel):
    __tablename__ = "deviceshadow"

    device_id = db.Column(db.String(255), primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    shadow_metadata = db.Column(JsonEncodedDict)

    def __init__(self, device_id):
        self.device_id = device_id

    def json(self):
        return {
                "id": self.id,
                "device_id": self.device_id,
                "shadow_metadata": self.shadow_metadata,
                "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
                }

    @classmethod
    def find_by_device_id(cls, device_id):
        return cls.query.filter_by(device_id=device_id).first()

