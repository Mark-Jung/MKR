import json
from flask import request
from flask.views import MethodView

from controllers.ListToCartController import ListToCartController 
from utils.parser import ReqParser
from utils.auth import Auth

class ListToCartView(MethodView):
   
    @classmethod
    def delete_list(cls):
        err, status, member_id, fam_id = Auth.whoisit(request.headers)
        if err:
            return json.dumps({"error_message": err}), 400

        data = json.loads(request.data.decode('utf-8'))
        req_params = ["victim_ids"]
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status, response = ListToCartController.delete_list(fam_id, data['victim_ids'])
        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": list(map(lambda x : x.json() if x else None, response))}), status

    @classmethod
    def delete_cart(cls):
        err, status, member_id, fam_id = Auth.whoisit(request.headers)
        if err:
            return json.dumps({"error_message": err}), 400

        data = json.loads(request.data.decode('utf-8'))
        req_params = ["victim_ids"]
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status, response = ListToCartController.delete_cart(fam_id, data['victim_ids'])
        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": list(map(lambda x : x.json() if x else None, response))}), status

    @classmethod
    def edit_list_to_cart(cls):
        err, status, member_id, fam_id = Auth.whoisit(request.headers)
        if err:
            return json.dumps({"error_message": err}), 400

        data = json.loads(request.data.decode('utf-8'))
        
        req_params = ["alias", "in_cart", "in_store", "item_name", "item_image", "item_price", "item_quantity", "list_to_cart_id"]
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status = ListToCartController.edit_list_to_cart(fam_id, data)
        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": "Success"}), status

    @classmethod
    def switch_list_to_cart(cls):
        err, status, member_id, fam_id = Auth.whoisit(request.headers)
        if err:
            return json.dumps({"error_message": err}), 400

        data = json.loads(request.data.decode('utf-8'))

        req_params = ["list_to_cart_id"]
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status = ListToCartController.switch_list_to_cart(fam_id, data['list_to_cart_id'])

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": "Success!"}), status

    @classmethod
    def get_cart(cls):
        err, status, member_id, fam_id = Auth.whoisit(request.headers)
        if err:
            return json.dumps({"error_message": err}), 400

        error_message, status, response = ListToCartController.get_cart(fam_id)
        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": list(map(lambda x : x.json() if x else None, response))}), status
   
    @classmethod
    def get_list(cls):
        err, status, member_id, fam_id = Auth.whoisit(request.headers)
        if err:
            return json.dumps({"error_message": err}), 400

        error_message, status, response = ListToCartController.get_list(fam_id)
        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": list(map(lambda x : x.json() if x else None, response))}), status

    @classmethod
    def register_list_to_cart(cls):
        err, status, member_id, fam_id = Auth.whoisit(request.headers)
        if err:
            return json.dumps({"error_message": err}), 400

        data = json.loads(request.data.decode('utf-8'))
        req_params = ["alias", "in_store"]
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status = ListToCartController.register_list(member_id, fam_id, data['alias'], data['in_store'])

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": "Success!"}), status
