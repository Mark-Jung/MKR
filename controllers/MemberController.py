import asyncio
from datetime import datetime
import os 
from random import *
import string

from models.CheckoutModel import CheckoutModel
from models.FamilyModel import FamilyModel
from models.MemberModel import MemberModel
from models.VerificationModel import VerificationModel

from utils.logger import Logger
from utils.email import Emailer

class MemberController():
    logger = Logger(__name__)

    @classmethod 
    def get_profile(cls, fam_id, member_id):
        member = MemberModel.find_by_id(member_id)
        family = FamilyModel.find_by_id(fam_id)
        # get first, last name from member
        first_name = member.first_name
        last_name = member.last_name
        # get admin_invite and member invite from family
        admin_invite = family.admin_invite
        member_invite = family.member_invite

        total = 0
        all_checkout = []
        # get family total(run through checkout)
        try:
            fam_checkout = CheckoutModel.filter_by_fam_id(fam_id)
            for each in fam_checkout:
                all_checkout.append(each.json())
                total += each.total
        except:
            cls.logger.exception("Error in getting all checkouts by family")
            return "Internal Server Error", 500, None
        result = {
            "first_name": first_name,
            "last_name": last_name,
            "total": total,
            "admin_invite": admin_invite,
            "member_invite": member_invite,
            "order_history": all_checkout,
        }
        return "", 200, result

    @classmethod
    def register_member(cls, data):
        # check if family with the same name exist
        member_already = MemberModel.find_by_email(data['email'])
        if member_already:
            return "Try a different E-mail", 400, None
        member_already = MemberModel.find_by_phone(data['phone'])
        if member_already:
            return "Try a different Phone number", 400, None

        try: 
            new_member = MemberModel(data['first_name'], data['last_name'], data['email'], data['phone'], data['password'])

            if os.environ.get("SECRET", "dev") == "dev":
                rand_string = "test"
            else:
                valid = True
                alphanums = string.digits + string.ascii_lowercase
                while valid:
                    rand_string = ""
                    for i in range(7):
                        rand_string += choice(alphanums)
                    if not VerificationModel.find_by_value(rand_string):
                        valid = False
            new_member.save_to_db()
            new_verification = VerificationModel(rand_string, new_member.id)
            new_verification.save_to_db()
        except:
            cls.logger.exception("Error creating a member.")
            return "Internal Server Error", 500, None

        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                asyncio.set_event_loop(asyncio.new_event_loop())
        except:
            asyncio.set_event_loop(asyncio.new_event_loop())
        
        loop = asyncio.get_event_loop()

        # send verification code to who registered
        tasks = [
            asyncio.ensure_future(Emailer.send_verification(new_member.email, new_member.first_name, new_verification.value))
        ]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

        return "", 201, new_member.generate_token()

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
            return "An account doesn't exist with this email.", 400, None

    @classmethod
    def update_token(cls, token):
        try:
            updated_token = MemberModel.update_token(token)
            return "", 200, updated_token
        except:
            cls.logger("Error in updating token")
            return "Internal Server Error", 500, None

    @classmethod
    def verify_member(cls, verification, member_id):
        all_verifications = VerificationModel.filter_by_member_id(member_id)
        verified = False
        for each in all_verifications:
            if each.value == verification:
                verified = True
                break
            
        if verified:
            member = MemberModel.find_by_id(member_id)
            member.verified = True
            member.save_to_db()
            for each in all_verifications:
                each.delete_from_db()
            return "", 200
        else:
            return "Failed to verify", 400
