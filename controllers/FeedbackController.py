import asyncio
from twilio.twiml.voice_response import VoiceResponse

from models.MemberModel import MemberModel

from utils.logger import Logger
from utils.email import Emailer

class FeedbackController():
    logger = Logger(__name__)

    @classmethod
    def record_feedback(cls):

        """Returns TwiML which prompts the caller to record a message"""
        # Start our TwiML response
        response = VoiceResponse()

        # Use <Say> to give the caller some instructions
        response.say('Hello, Niche always welcomes feedback so thank you for your time and effort. Press pound to end your recording. We will start recording after the beep.')

        # Use <Record> to record the caller's message
        response.record(finishOnKey='#', transcribe=True, timeout=0)

        # End the call with <Hangup>
        response.hangup()

        # record link, member_id(by phone number), transcription_link

        print(str(response))
        

        # send eamil
        # if asyncio.get_event_loop().is_closed():
        #     asyncio.set_event_loop(asyncio.new_event_loop())
        # loop = asyncio.get_event_loop()
        # # send email to alert team
        # tasks = [asyncio.ensure_future(Emailer.feedback(string(response))]
        # loop.run_until_complete(asyncio.wait(tasks))
        # loop.close()

        return "", 201, str(response)
