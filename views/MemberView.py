from flask import request
from flask.views import MethodView
from controllers.MemberController import MemberController
from utils.parser import ReqParser

import json

class MemberView(MethodView):
    
    @classmethod
    def register_member(cls):
        data = json.loads(request.data.decode('utf-8'))
        req_params = ["first_name", "last_name", "email", "invite_code", "authority", "password"]
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status, response = MemberController.register_member(data)

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": response}), status
