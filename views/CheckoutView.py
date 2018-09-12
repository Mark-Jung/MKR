from flask import request
from flask.views import MethodView

from controllers.CheckoutController import CheckoutController
from utils.parser import ReqParser
from utils.auth import Auth

import json

class CheckoutView(MethodView):
    
    @classmethod
    def checkout(cls):
        err, status, member_id, fam_id = Auth.whoisit(request.headers)
        if err:
            return json.dumps({"error_message": err}), status

        data = json.loads(request.data.decode('utf-8'))
        req_params = ['total', 'items']
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status = CheckoutController.checkout(member_id, fam_id, data['total'], data['items'])

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": "Success!"}), 200
