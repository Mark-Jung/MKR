import os, sys
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
basedir = os.path.abspath(os.path.dirname(__file__))
from app import app
from db import db
import json
from datetime import datetime, timedelta

from helper import Helper

TEST_DB = 'test.db'

class UserTests(unittest.TestCase):
    family_info = {
        "address_line1": "he",
        "address_line2": "ll",
        "city": "evanston",
        "state": "il",
        "zip_code": 63127,
        "name": "niche",
    }

    member_info = {
        "email": "niche@niche.io",
        "phone": "+17365331363",
        "first_name": "niche",
        "last_name": "nichel",
        "password": "nicolo"
    }

    member_info1 = {
        "email": "member1@niche.io",
        "phone": "+17365331364",
        "first_name": "niche",
        "last_name": "nichel",
        "password": "nicolo"
    }

    invite_emails = {
        "admin": ["gujung2022@test.edu"],
        "member": ["gujung2022@test.edu"],
    }




    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.init_app(app)
        db.drop_all(app=app)
        db.create_all(app=app)


    # executed after each test
    def tearDown(self):
        pass

    def test_member_family_signupflow(self):
        # create member
        member = self.app.post('/member/register', data=json.dumps(self.member_info))
        member_token = json.loads(member.data.decode())['token']
        self.assertEqual(201, member.status_code)

        # verify email for member
        verify = self.app.post('/verify',
            data=json.dumps({"verification_code": "test"}),
            headers=dict(
                Authorization="Bearer " + member_token,
                content_type="application/json"
            ))
        self.assertEqual(200, verify.status_code)

        # create family
        family = self.app.post('/family/register',
            data=json.dumps(self.family_info),
            headers=dict(
                Authorization="Bearer " + member_token,
                content_type="application/json"
            ))
        self.assertEqual(201, family.status_code)
        family_invite = json.loads(family.data.decode())['response']
        admin_invite = family_invite['admin']
        member_invite = family_invite['member']

        # invite
        invite = self.app.post('/invite',
            data=json.dumps(self.invite_emails),
            headers=dict(
                Authorization="Bearer " + member_token,
                content_type="application/json"
            ))
        self.assertEqual(200, invite.status_code)

        # signin
        token = self.app.post('/signin', data=json.dumps({"email":self.member_info["email"], "password":self.member_info["password"]}))
        self.assertEqual(200, token.status_code)

        # create another member
        member = self.app.post('/member/register', data=json.dumps(self.member_info1))
        member_token = json.loads(member.data.decode())['token']
        self.assertEqual(201, member.status_code)

        # verify email for member
        verify = self.app.post('/verify',
            data=json.dumps({"verification_code": "test"}),
            headers=dict(
                Authorization="Bearer " + member_token,
                content_type="application/json"
            ))
        self.assertEqual(200, verify.status_code)

        # join family as member
        join = self.app.post('/family/join',
            data=json.dumps({"invite_code": member_invite}),
            headers=dict(
                Authorization="Bearer " + member_token,
                content_type="application/json"
            ))
        self.assertEqual(200, join.status_code)
        join_data = json.loads(join.data.decode())
        self.assertEqual('niche', join_data['response'])