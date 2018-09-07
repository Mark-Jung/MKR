from datetime import datetime
import asyncio

from models.MemberModel import MemberModel
from models.FamilyModel import FamilyModel

from utils.logger import Logger
from utils.email import Emailer

class MemberController():
    logger = Logger(__name__)

    @classmethod
    def register_member(cls, data):
        # check if family with the same name exist
        member_already = MemberModel.find_by_email(data['email'])
        if member_already:
            return "Ill-formed Reqeust", 400, None
        
        family = FamilyModel.find_by_invite_admin(data['invite_code'])
        if family:
            fam_id = family.id
            invite_code_admin = family.admin_invite
            invite_code_member = family.member_invite
            authority = 100
        else:
            family = FamilyModel.find_by_invite_member(data['invite_code'])
            if family:
                fam_id = family.id
                authority = 50
            else:
                cls.logger.exception("Invalid invite_code")
                return "Ill-formed Request", 400, None

        try: 
            new_member = MemberModel(data['first_name'], data['last_name'], data['email'], fam_id, authority, data['password'])
            new_member.save_to_db()
        except:
            cls.logger.exception("Error creating a member.")
            return "Internal Server Error", 500, None

        if asyncio.get_event_loop().is_closed():
            asyncio.set_event_loop(asyncio.new_event_loop())

        loop = asyncio.get_event_loop()
        
        # send email to who registered
        if authority == 50:
            # no need to send invite codes
            tasks = [
                asyncio.ensure_future(Emailer.signup(new_member.email, new_member.first_name, "", "", family.name))
            ]
        elif authority == 100:
            # send invite codes
            tasks = [
                asyncio.ensure_future(Emailer.signup(new_member.email, new_member.first_name, family.admin_invite, family.member_invite, family.name))
            ]
        else:
            cls.logger.exception("Value of authority is not as expected.")
            return "Internal Server Error", 500, None
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

        return "", 201, 

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
    