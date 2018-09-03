from datetime import datetime
import string
from random import *

from models.FamilyModel import FamilyModel
from utils.logger import Logger

class FamilyController():
    promo_length = 8
    allchar = string.ascii_letters + string.digits
    logger = Logger(__name__)

    @classmethod
    def register_family(cls, data):
        # check if family with the same name exist
        fam_already = FamilyModel.find_by_name(data['name'])
        if fam_already:
            return "Ill-formed Reqeust. Name should be unique", 400, None

        try: 
            admin_invite = FamilyController.generate_invite(data['name'] + '_admin_')
            member_invite = FamilyController.generate_invite(data['name'] + '_member_')
            new_fam = FamilyModel(data['address_line1'], data['address_line2'], data['city'], data['state'], data['zip_code'], data['name'], data['phone'], data['email'], admin_invite, member_invite)
            new_fam.save_to_db()
        except:
            cls.logger.exception("Error creating a family model")
            return "Internal Server Error", 500, None

        return "", 201, {"admin": new_fam.admin_invite, "member": new_fam.member_invite}
    
    @classmethod
    def generate_invite(cls, keyword):
        found = False
        new_invite = keyword
        while not found:
            for x in range(cls.promo_length):
                new_invite += choice(cls.allchar)
            if FamilyModel.find_by_invite_admin(new_invite) is None and FamilyModel.find_by_invite_member(new_invite) is None:
                found = True
            else:
                new_invite = keyword
            
        return new_invite
    