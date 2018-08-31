from flask import request
from flask.views import MethodView
from controllers.FamilyController import FamilyController
from utils.parser import ReqParser

import json

class FamilyView(MethodView):
    
    @classmethod
    def register_family(cls):
        data = json.loads(request.data.decode('utf-8'))
        req_params = ['address_line1', 'address_line2', 'city', 'state', 'zip_code', 'phone', 'email', 'name']
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status, family_id = FamilyController.register_family(data)

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": family_id}), status
