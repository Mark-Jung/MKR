from models.MemberModel import MemberModel

class Auth():
    """
    consumes the header and returns 0(invalid) or member id(valid)
    """
    @classmethod
    def whoisit(cls, headers):
        auth_header = headers.get('Authorization')
        if auth_header:
            access_token = auth_header.split(" ")[1]
        else:
            return -1
        error_message, member_id = MemberModel.decode_token(access_token)
        if error_message:
            return 0
        else:
            return member_id
        