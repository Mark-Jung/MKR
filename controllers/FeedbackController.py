import asyncio
from twilio.twiml.voice_response import VoiceResponse

from models.MemberModel import MemberModel
from models.FeedbackModel import FeedbackModel

from utils.logger import Logger
from utils.email import Emailer

class FeedbackController():
    logger = Logger(__name__)

    @classmethod
    def respond_feedback(cls):
        """Returns TwiML which prompts the caller to record a message"""
        # Start our TwiML response
        response = VoiceResponse()

        # Use <Say> to give the caller some instructions
        response.say('Hello, Niche always welcomes feedback so thank you for your time and effort. End the call after you are done. We will start recording after the beep.')

        # Use <Record> to record the caller's message
        response.record(action="/feedback/save", finishOnKey='', timeout=0)

        # End the call with <Hangup>
        response.hangup()

        return str(response), 200

    @classmethod
    def save_feedback(cls, caller, record_url, record_duration):
        # make feedback model
        member = MemberModel.find_by_phone(caller)
        if not member:
            cls.logger.exception("Called from a non-member.")
            return "Ill-formed Request", 400, None

        try:
            new_feedback = FeedbackModel(record_duration, record_url, "", member.id)
            new_feedback.save_to_db()
        except:
            cls.logger.exception("Error in creating a feedback model")
            return "Internal Server Error", 500, None
        
        # send eamil with feedback link
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                asyncio.set_event_loop(asyncio.new_event_loop())
        except:
            asyncio.set_event_loop(asyncio.new_event_loop())
        
        loop = asyncio.get_event_loop()
        # send email to alert Umur, Ivan, Chris, and me
        tasks = [asyncio.ensure_future(Emailer.feedback(record_url, record_duration, member.first_name + ' ' + member.last_name, member.fam_id))]

        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
        return "", 201, "Success"

