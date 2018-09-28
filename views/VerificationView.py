from flask import request
from flask.views import MethodView
from controllers.VerificationController import VerificationController
from utils.parser import ReqParser
from utils.auth import Auth

import json

class VerificationView(MethodView):
    
    @classmethod
    def verify_member(cls):
        err, status, member_id, fam_id = Auth.whoisit(request.headers)
        if err and err != 'Not a verified member':
            return json.dumps({"error_message": err}), status

        data = json.loads(request.data.decode('utf-8'))
        req_params = ["verification_code"]
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400
        error_message, status = VerificationController.verify_member(data['verification_code'], member_id)

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": "Success!"}), status 

    @classmethod
    def resend_verification(cls):
        err, status, member_id, fam_id = Auth.whoisit(request.headers)
        if err and err != 'Not a verified member':
            return json.dumps({"error_message": err}), status

        error_message, status = VerificationController.resend_verification(member_id)

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": "Success!"}), status 
        