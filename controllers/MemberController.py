from datetime import datetime

from models.MemberModel import MemberModel
from utils.logger import Logger

class FamilyController():
    logger = Logger(__name__)

    @classmethod
    def register_member(cls, data):
        # check if family with the same name exist
        member_already = MemberModel.find_by_email(data['email'])
        if member_already:
            return "Ill-formed Reqeust", 400
        
        no_invite = 

        try: 
            new_member = MemberModel(data['first_name'], data['last_name'], data['email'], data['family_name'], data['authority'], data['password'])
            new_member.save_to_db()
        except:
            cls.logger.exception("Error creating a member.")
            return "Internal Server Error", 500

        return "", 201


    