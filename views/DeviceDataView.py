from flask import request
from flask.views import MethodView
from controllers.DeviceDataController import DeviceDataController
from utils.parser import ReqParser

import json

class DeviceDataView(MethodView):

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
    def get_all(cls):
        error_message, status, response = DeviceDataController.get_all()

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": ReqParser.as_jsonlist(response)}), status

    @classmethod
    def register_device(cls):
        data = json.loads(request.data.decode('utf-8'))
        req_params = ['device_id', 'shadow_metadata', 'alert_level', 'container', 'alias', 'auto_order_store', 'product_metadata']
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status = DeviceDataController.create_shadow(data['device_id'], data['shadow_metadata'], data['alert_level'], data['container'], data['alias'], data['auto_order_store'], data['product_metadata'])

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": "Success"}), status

    @classmethod
    def get_niches(cls):
        data = json.loads(request.data.decode('utf-8'))
        req_params = ['niche_ids']
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status, response = DeviceDataController.get_shadows(data['niche_ids'])

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": list(map(lambda x : x.json() if x else None, response))}), status

