import os
import smtplib
import asyncio
from utils.bodybuilder import BodyBuilder
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Emailer():
    recipients = [os.environ.get("dev_email", "gujung2022@u.northwestern.edu")]
    @classmethod
    def send_email(cls, msg, recipients):
        # Send the message via gmail's SMTP server.
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        # os environment var for password
        if os.environ.get("SECRET", "wow") == "wow":
            print("sent mail successfully!")
            s.login(os.environ['email'], os.environ['password'])
            for each in recipients:
                s.sendmail("nichesapphire@gmail.com", each, msg.as_string())
        else:
            s.login(os.environ['email'], os.environ['password'])
            for each in recipients:
                s.sendmail("nichesapphire@gmail.com", each, msg.as_string())
        s.quit()

    @classmethod
    async def signup(cls, email, name, admin_invite, member_invite, fam_name):
        if os.environ.get("SECRET", "dev") == 'dev':
            customer = [os.environ['dev_email']]
        else:
            customer = [str(email)]

        msg = MIMEMultipart('alternative')
        msg.add_header('Content-Type', 'text/html; charset=utf-8')
        msg['Subject'] = 'Welcome to Niche!'
        if admin_invite == "":
            body = BodyBuilder.signup_joinfam(name, fam_name)
        else:
            body = BodyBuilder.signup_createfam(name, admin_invite, member_invite, fam_name)
        HTML_BODY = MIMEText(body, 'html')
        msg.attach(HTML_BODY)

        cls.send_email(msg, customer)
 
    @classmethod
    async def invite(cls):
        pass
               
    @classmethod 
    async def checkout(cls):
        pass
