import os
import smtplib
import asyncio
from utils.bodybuilder import BodyBuilder
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Emailer():
    recipients = [os.environ.get("dev_email", "gujung2022@u.northwestern.edu")]
    @classmethod
    def send_email(cls, subject, body, recipients):
        # send to dev email if testing
        if os.environ.get("SECRET", "dev") == 'dev':
            recipients = [os.environ["dev_email"]]

        # make message
        msg = MIMEMultipart('alternative')
        msg.add_header('Content-Type', 'text/html; charset=utf-8')
        msg['Subject'] = subject
        msg.attach(body)

        # Send the message via gmail's SMTP server.
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        # os environment var for password
        if os.environ.get("SECRET", "wow") == "wow":
            print("sent mail successfully!")
            # s.login(os.environ['email'], os.environ['password'])
            # for each in recipients:
            #     s.sendmail("nichesapphire@gmail.com", each, msg.as_string())
        else:
            s.login(os.environ['email'], os.environ['password'])
            for each in recipients:
                s.sendmail("nichesapphire@gmail.com", each, msg.as_string())
        s.quit()

    @classmethod 
    async def checkout(cls, total, member_name, family_name, items, checkout_id):
        recipients = ["iec@u.northwestern.edu", "umur@u.northwestern.edu"]
        body = BodyBuilder.alert_order(total, member_name, family_name, items, checkout_id)
        HTML_BODY = MIMEText(body, 'html')

        cls.send_email("GO FULFILL THE NICHE ORDER!!!!!!!", HTML_BODY, recipients)
        
    @classmethod 
    async def create_fam(cls, email, name, admin_invite, member_invite, fam_name):
        body = BodyBuilder.signup_createfam(name, admin_invite, member_invite, fam_name)
        HTML_BODY = MIMEText(body, 'html')

        cls.send_email("Welcome to Niche!", HTML_BODY, [email])

    @classmethod
    async def feedback(cls, record_url, record_duration, member_name, fam_id):
        recipients = ["iec@u.northwestern.edu", "umur@u.northwestern.edu", "gujung2022@u.northwestern.edu", "Datschris222@gmail.com"]
        body = BodyBuilder.alert_feedback(record_url, record_duration, member_name, fam_id)
        HTML_BODY = MIMEText(body, 'html')

        cls.send_email("Feedback has been recorded from " + member_name, HTML_BODY, recipients)
 
    @classmethod
    async def invite(cls, admin_invite, member_invite, fam_name, admins, members):
        admin_body = BodyBuilder.invite(admin_invite, fam_name, "admin")
        ADMIN_HTML = MIMEText(admin_body, 'html')

        member_body = BodyBuilder.invite(member_invite, fam_name, "member")
        MEMBER_HTML = MIMEText(member_body, 'html')

        cls.send_email("Invitation to Niche", ADMIN_HTML, admins)
        cls.send_email("Invitation to Niche", MEMBER_HTML, members)
               
    @classmethod
    async def join_fam(cls, email, name, fam_name):
        body = BodyBuilder.signup_joinfam(name, fam_name)
        HTML_BODY = MIMEText(body, 'html')

        cls.send_email("Welcome to Niche!", HTML_BODY, [email]) 
 
    @classmethod
    async def send_verification(cls, email, name, code):
        body = BodyBuilder.verification(name, code)
        HTML_BODY = MIMEText(body, 'html')

        cls.send_email("Verify your account -Niche", HTML_BODY, [email])