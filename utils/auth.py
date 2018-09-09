from models.MemberModel import MemberModel
from models.FamilyModel import FamilyModel

from utils.logger import Logger

class Auth():
    logger = Logger(__name__)
    """
    consumes the header and returns 0(invalid) or member id(valid)
    """
    @classmethod
    def whoisit(cls, headers):
        auth_header = headers.get('Authorization')
        if auth_header:
            access_token = auth_header.split(" ")[1]
        else:
            return -1, -1
        error_message, member_id = MemberModel.decode_token(access_token)
        if error_message:
            return 0, 0
        else:
            try:
                member = MemberModel.find_by_id(member_id)
                fam_id = member.fam_id
            except:
                cls.logger.exception("Non-existing member")
                return -1, -1

            return member_id, fam_id
        