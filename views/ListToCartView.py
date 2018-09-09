import json
from flask import request
from flask.views import MethodView

from controllers.ListToCartController import ListToCartController 
from utils.parser import ReqParser
from utils.auth import Auth

class ListToCartView(MethodView):
    
    @classmethod
    def register_list(cls):
        member_id, fam_id = Auth.whoisit(request.headers)
        if member_id < 0:
            return json.dumps({"error_message": "ill-formed request"}), 400
        elif member_id == 0:
            return json.dumps({"error_message": "Not Authorized"}), 403

        data = json.loads(request.data.decode('utf-8'))
        req_params = ["alias", "in_store"]
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status = ListToCartController.register_list(member_id, fam_id, data['alias'], data['in_store'])

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": "Success!"}), status

    @classmethod
    def register_cart(cls):
        member_id, fam_id = Auth.whoisit(request.headers)
        if member_id < 0:
            return json.dumps({"error_message": "ill-formed request"}), 400
        elif member_id == 0:
            return json.dumps({"error_message": "Not Authorized"}), 403

        data = json.loads(request.data.decode('utf-8'))

        req_params = ["in_store", "item_name", "item_image", "item_price", "item_quantity", "list_to_cart_id"]
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status = ListToCartController.register_cart(data)

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": "Success!"}), status

