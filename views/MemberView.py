from flask import request
from flask.views import MethodView
from controllers.MemberController import MemberController
from utils.parser import ReqParser
from utils.auth import Auth

import json

class MemberView(MethodView):
    
    @classmethod
    def register_member(cls):
        data = json.loads(request.data.decode('utf-8'))
        req_params = ["first_name", "last_name", "email", "password", "phone"]
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status, token = MemberController.register_member(data)

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"token": token}), status
    
    @classmethod
    def signin(cls):
        data = json.loads(request.data.decode('utf-8'))
        req_params = ['email', 'password']
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status, token = MemberController.signin(data)

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"token": token}), 200

    @classmethod
    def signin_by_token(cls):
        err, status, member_id, fam_id = Auth.whoisit(request.headers)
        if err and member_id == 0:
            return json.dumps({"error_message": err}), status
        else:
            return json.dumps({"response": err}), 200
        
        auth_header = headers.get('Authorization')

        error_message, status, token = MemberController.update_token(auth_header.split(" ")[1])

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": token}), status 
