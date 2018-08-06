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

        return "", 201


    @classmethod
    def create_shadow(cls, device_id):
        if DeviceShadowModel.find_by_device_id(device_id):
            cls.logger.exception("Tried to create a shadow with the same niche_id")
            return "Invalid Request", 400 
        
        try:
            new_shadow = DeviceShadowModel(device_id)
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
            return "Internal System Error", 500, None
        return "", 200, all_device_data

