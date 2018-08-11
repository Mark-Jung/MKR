from datetime import datetime

from models.DeviceDataModel import DeviceDataModel
from models.DeviceShadowModel import DeviceShadowModel
from utils.logger import Logger

class DeviceDataController():
    logger = Logger(__name__)

    @classmethod
    def collect_data(cls, device_id, metadata):
        target_device = DeviceShadowModel.find_by_device_id(device_id)
        if not target_device:
            cls.logger.exception("Tried to add a stamp of a device that doesn't exist")
            return "Invalid Request", 400
        try:
            new_stamp = DeviceDataModel(device_id, metadata)
            new_stamp.save_to_db()
        except:
            cls.logger.exception("Error while creating a new stamp in the Device Data Model")
            return "Internal Server Error", 500
        
        if target_device.date_updated < new_stamp.date_created:
            try:
                target_device.shadow_metadata = new_stamp.device_metadata
                target_device.date_updated = new_stamp.date_created
                target_device.save_to_db()
            except:
                cls.logger.exception("Error while saving most recent")

        return "", 201


    @classmethod
    def create_shadow(cls, device_id, shadow_metadata, alert_level, container, alias):
        if DeviceShadowModel.find_by_device_id(device_id):
            cls.logger.exception("Tried to create a shadow with the same niche_id")
            return "Invalid Request", 400 
        
        try:
            new_shadow = DeviceShadowModel(device_id, shadow_metadata, alert_level, container, alias)
            new_shadow.save_to_db()
        except:
            cls.logger.exception("Error while creating Device Shadow")
            return "Internal Server Error", 500

        return "", 201

    @classmethod 
    def get_all(cls):
        try:
            all_device_data = DeviceDataModel.get_all()
        except:
            cls.logger.exception("Error in getting data for all devices")
            return "Internal Server Error", 500, None
        return "", 200, all_device_data

    @classmethod
    def get_shadows(cls, shadow_ids):
        result = []
        for shadow_id in shadow_ids:
            target_shadow = DeviceShadowModel.find_by_device_id(shadow_id)
            if target_shadow:
                result.append(target_shadow)
            else:
                return "Ill-formed Request", 400, None
        return "", 200, result
        