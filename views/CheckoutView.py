from flask import request
from flask.views import MethodView

from controllers.CheckoutController import CheckoutController
from utils.parser import ReqParser
from utils.auth import Auth

import json

class CheckoutView(MethodView):
    
    @classmethod
    def checkout(cls):
        member_id, fam_id = Auth.whoisit(request.headers)
        if member_id < 0:
            return json.dumps({"error_message": "ill-formed request"}), 400
        elif member_id == 0:
            return json.dumps({"error_message": "Not Authorized"}), 403
        data = json.loads(request.data.decode('utf-8'))
        req_params = ['total', 'items']
        req_params_item = ['store', 'price', 'url', 'name']
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400
        for item in data['items']:
            if not ReqParser.check_body(item, req_params_item):
                return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status = CheckoutController.checkout(member_id, data)

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": "Success!"}), 200
