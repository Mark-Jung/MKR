from flask import request
from flask.views import MethodView
from controllers.FeedbackController import FeedbackController

from utils.parser import ReqParser
from utils.auth import Auth

import json

class FeedbackView(MethodView):

    @classmethod
    def record_feedback(cls):
        data = json.loads(request.data.decode('utf-8'))
        if not ReqParser.check_body(data, req_params):
            return json.dumps({"error_message": "ill-formed request"})

        error_message, status = FamilyController.invite_by_email(data['admin'], data['member'], fam_id)

        if error_message:
            return json.dumps({"error_message": error_message}), status
        return json.dumps({"response": "Success"}), status
