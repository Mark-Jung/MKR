import json
from flask import request
from flask.views import MethodView

from controllers.DeviceDataController import DeviceDataController
from utils.parser import ReqParser
from utils.auth import Auth


class DeviceDataView(MethodView):
    @classmethod
    def claim_niche(cls):
        err, status, member_id, fam_id = Auth.whoisit(request.headers)
        if err:
            return json.dumps({"error_message": err}), 400
        

        data = json.loads(request.data.decode('utf-8'))
        req_params = ['device_id', 'alert_level', 'container', 'alias', 'auto_order_store', 'product_metadata']
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status = DeviceDataController.claim_niche(fam_id, data)

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": "Success"}), status

 
    @classmethod
    def collect_data(cls):
        data = json.loads(request.data.decode('utf-8'))
        req_params = ['device_id', 'metadata']
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status = DeviceDataController.collect_data(data['device_id'], data['metadata'])

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": "Success"}), status

    @classmethod
    def edit_niche(cls):
        err, status, member_id, fam_id = Auth.whoisit(request.headers)
        if err:
            return json.dumps({"error_message": err}), 400

        data = json.loads(request.data.decode('utf-8'))
        req_params = ['device_id', 'alert_level', 'container', 'alias', 'auto_order_store', 'product_metadata']
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status = DeviceDataController.edit_niche(fam_id, data)

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": "Success"}), status

    @classmethod
    def get_all(cls):
        error_message, status, response = DeviceDataController.get_all()

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": ReqParser.as_jsonlist(response)}), status

    @classmethod
    def register_device(cls):
        # Requires factory reset auth, super user authority

        data = json.loads(request.data.decode('utf-8'))
        req_params = ['device_id']
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status = DeviceDataController.create_shadow(data['device_id'])

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": "Success"}), status

    @classmethod
    def get_niches(cls):
        err, status, member_id, fam_id = Auth.whoisit(request.headers)
        if err:
            return json.dumps({"error_message": err}), 400

        error_message, status, response = DeviceDataController.get_shadows(fam_id)

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": list(map(lambda x : x.json() if x else None, response))}), status
