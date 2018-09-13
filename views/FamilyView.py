from flask import request
from flask.views import MethodView
from controllers.FamilyController import FamilyController

from utils.parser import ReqParser
from utils.auth import Auth

import json

class FamilyView(MethodView):

    @classmethod
    def invite_by_email(cls):
        err, status, member_id, fam_id = Auth.whoisit(request.headers)
        if err:
            return json.dumps({"error_message": err}), 400
        
        data = json.loads(request.data.decode('utf-8'))
        req_params = ['admin', 'member']
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"})

        error_message, status = FamilyController.invite_by_email(data['admin'], data['member'], fam_id)

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": "Success"}), status

    @classmethod
    def join_family(cls):
        err, status, member_id, fam_id = Auth.whoisit(request.headers)
        if err and err != 'Not registered to family':
            return json.dumps({"error_message": err}), 400

        data = json.loads(request.data.decode('utf-8'))
        req_params = ['invite_code']
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status = FamilyController.join_family(data['invite_code'], member_id)

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": "Success"}), status
    
    @classmethod
    def register_family(cls):
        err, status, member_id, fam_id = Auth.whoisit(request.headers)
        if err and err != 'Not registered to family':
            return json.dumps({"error_message": err}), 400

        data = json.loads(request.data.decode('utf-8'))
        req_params = ['address_line1', 'address_line2', 'city', 'state', 'zip_code', 'phone', 'name']
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status, response = FamilyController.register_family(data, member_id)

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": response}), status
