from datetime import datetime

from models.MemberModel import MemberModel
from models.FamilyModel import FamilyModel
from utils.logger import Logger

class MemberController():
    logger = Logger(__name__)

    @classmethod
    def register_member(cls, data):
        # check if family with the same name exist
        member_already = MemberModel.find_by_email(data['email'])
        if member_already:
            return "Ill-formed Reqeust", 400
        
        admin_invite = FamilyModel.find_by_invite_admin(data['invite_code'])
        if admin_invite:
            fam_id = admin_invite.id
            authority = 100
        else:
            member_invite = FamilyModel.find_by_invite_member(data['invite_code'])
            if member_invite:
                fam_id = member_invite.id
                authority = 50
            else:
                cls.logger.exception("Invalid invite_code")
                return "Ill-formed Request", 400
        try: 
            new_member = MemberModel(data['first_name'], data['last_name'], data['email'], fam_id, authority, data['password'])
            new_member.save_to_db()
        except:
            cls.logger.exception("Error creating a member.")
            return "Internal Server Error", 500

        return "", 201

    @classmethod
    def signin(cls, data):
        member = MemberModel.find_by_email(data['email'])
        if member:
            if member.validate_password(data['password']):
                try:
                    token = member.generate_token()
                except:
                    cls.logger.exception("Error generating token")
                    return "", 500, None
                return "", 200, token
            else:
                return "Invalid combination", 403, None
        else:
            return "Ill-formed Request", 400, None
    