from models.MemberModel import MemberModel
from models.FamilyModel import FamilyModel

from utils.logger import Logger

class Auth():
    logger = Logger(__name__)
    """
    consumes the header
    returns an error message, status, and two numbers in a tuple: (member_id, fam_id)
    """
    @classmethod
    def whoisit(cls, headers):
        auth_header = headers.get('Authorization')
        if auth_header:
            access_token = auth_header.split(" ")[1]
        else:
            return "No Authorization header", 400, 0, 0
        error_message, member_id = MemberModel.decode_token(access_token)
        if error_message:
            return error_message, 403, 0, 0
        else:
            try:
                member = MemberModel.find_by_id(member_id)
                if member == None:
                    cls.logger.exception("Non-existing member")
                    return "No such member with the id", 403, 0, 0   
                fam_id = member.fam_id
            except:
                cls.logger.exception("Non-existing member")
                return "Error finding member by id", 500, 0, 0
            
            
            if not member.verified:
                return "Not a verified member", 403, member.id, 0
            elif not fam_id:
                cls.logger.exception("Didn't join family yet")
                return "Not registered to family", 400, member.id, 0

            return "", 0, member_id, fam_id
        