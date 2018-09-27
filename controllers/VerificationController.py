import asyncio
from datetime import datetime
import os 
from random import *
import string

from models.FamilyModel import FamilyModel
from models.MemberModel import MemberModel
from models.VerificationModel import VerificationModel

from utils.logger import Logger
from utils.email import Emailer

class VerificationController():
    logger = Logger(__name__)

    @classmethod
    def verify_member(cls, verification, member_id):
        member = MemberModel.find_by_id(member_id)
        if member and member.verified:
            return "", 200

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
    
    @classmethod
    def resend_verification(cls, member_id):
        
        if os.environ.get("SECRET", "dev") == "dev":
            rand_string = "retest"
        else:
            try:
                valid = True
                alphanums = string.digits + string.ascii_lowercase
                rand_string = ""
                while valid:
                    rand_string = ""
                    for i in range(7):
                        rand_string += choice(alphanums)
                    if not VerificationModel.find_by_value(rand_string):
                        valid = False
            except:
                cls.logger.exception("Error while creating random string")
                return "Internal Server Error", 500
        try:
            new_verification = VerificationModel(rand_string, new_member.id)
            new_verification.save_to_db()
        except:
            cls.logger.exception("Error while saving to db")
            return "Internal Server Error", 500
    
        return "", 201 
    