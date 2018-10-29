from datetime import datetime

from models.DeviceDataModel import DeviceDataModel
from models.DeviceShadowModel import DeviceShadowModel
from models.ListToCartModel import ListToCartModel 
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
                if float(new_stamp.device_metadata['percent']) < target_device.alert_level:
                    # move that niche thing to list
                    # if the same name is in the listtocart, delete that item 
                    make = True
                    already = ListToCartModel.get_fam_list(target_device.fam_id)
                    for each in already:
                        if each.alias == target_device.alias:
                            each.from_niche = True
                            each.in_store = target_device.auto_order_store
                            each.save_to_db()
                            make = False
                            
                    if make:
                        try:
                            new_list_to_cart = ListToCartModel(target_device.alias, target_device.auto_order_store, target_device.fam_id, "Niche")
                            new_list_to_cart.from_niche = True
                            new_list_to_cart.save_to_db()
                        except:
                            cls.logger.exception("Error while moving niche into listtocart")
                            return "Internal Server Error", 500
                    
            except:
                cls.logger.exception("Error while saving most recent")
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
    def edit_niche(cls, fam_id, data):
        target_device = DeviceShadowModel.find_by_device_id(data['device_id'])
        if not target_device:
            cls.logger.exception("Tried to add a stamp of a device that doesn't exist")
            return "Invalid Request", 400
        
        if not target_device.fam_id:
            target_device.fam_id = fam_id
        elif target_device.fam_id != fam_id:
            cls.logger.exception("Tried to claim someone else's niche device")
            return "Invalid Request", 400

        fam_devices = DeviceShadowModel.filter_by_fam_id(fam_id)
        for each in fam_devices:
            if each.alias == data['alias'] and each.device_id != target_device.device_id :
                cls.logger.exception("Tried to make niches with duplicate names")
                return "Use different names for your niches", 400
        
        try:
            target_device.alert_level = data['alert_level']
            target_device.container = data['container']
            target_device.alias = data['alias']
            target_device.auto_order_store = data['auto_order_store']
            target_device.product_metadata = data['product_metadata']
            target_device.save_to_db()
        except:
            cls.logger.exception("Error in editing and saving initial niche info")
            return "Internal Server Error", 500

        return "", 200

    @classmethod 
    def get_all(cls):
        try:
            all_device_data = DeviceDataModel.get_all()
        except:
            cls.logger.exception("Error in getting data for all devices")
            return "Internal Server Error", 500, None
        return "", 200, all_device_data

    @classmethod
    def get_shadows(cls, fam_id):
        target_shadow = DeviceShadowModel.filter_by_fam_id(fam_id)
        return "", 200, target_shadow
        