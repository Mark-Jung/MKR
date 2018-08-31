from datetime import datetime

from models.FamilyModel import FamilyModel
from utils.logger import Logger

class FamilyController():
    logger = Logger(__name__)

    @classmethod
    def register_family(cls, data):
        # check if family with the same name exist
        fam_already = FamilyModel.find_by_name(data['name'])
        if fam_already:
            return "Ill-formed Reqeust", 400, None

        try: 
            new_fam = FamilyModel(data['address_line1'], data['address_line2'], data['city'], data['state'], data['zip_code'], data['name'], data['phone'], data['email'])
            new_fam.save_to_db()
        except:
            cls.logger.exception("Error creating a family model")
            return "Internal Server Error", 500, None

        return "", 201, new_fam.id


    