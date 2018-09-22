from flask import request
from flask.views import MethodView
from controllers.FeedbackController import FeedbackController

from utils.parser import ReqParser
from utils.auth import Auth

import json

class FeedbackView(MethodView):

    @classmethod
    def respond_feedback(cls):
        response, status= FeedbackController.respond_feedback()
        return response, status

    @classmethod
    def save_feedback(cls):
        # req_params = ['From', 'RecordingURL', 'RecordingDuration']
        # if not ReqParser.check_body(request.values, req_params):
        #     return json.dumps({"error_message": "ill-formed request"}), 400

        error_message, status, response = FeedbackController.save_feedback(request.values['From'], request.values['RecordingUrl'], request.values['RecordingDuration'])

        if error_message:
            return json.dumps({"error_message": error_message})
        return json.dumps({"response": response}), status