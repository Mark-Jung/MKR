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
        "phone": 1231231234,
        "email": "niche@niche.io",
        "name": "niche",
    }

    member_info = {
        "email": "niche@niche.io",
        "first_name": "niche",
        "last_name": "nichel",
        "password": "nicho"
    }

    checkout_info = {
        "total": 1000,
        "items": [{
            "store": "Walmart",
            "price": 5,
            "url": "hi",
            "name": "cat",
        }, {
            "store": "Walmart",
            "price": 5,
            "url": "hi",
            "name": "cat",
        }]
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
    
    def test_checkout(self):
        family = self.app.post('/family/register', data=json.dumps(self.family_info))
        self.assertEqual(201, family.status_code)
        family_data = json.loads(family.data.decode())

        self.member_info["invite_code"] = family_data['response']['admin']
        member = self.app.post('/member/register', data=json.dumps(self.member_info))
        self.assertEqual(201, member.status_code)

        token = self.app.post('/signin', data=json.dumps({"email":self.member_info["email"], "password":self.member_info["password"]}))
        self.assertEqual(200, token.status_code)
        access_token = json.loads(token.data.decode())['token']

        checkout = self.app.post('/checkout', 
        data=json.dumps(self.checkout_info), 
        headers=dict(
                Authorization="Bearer " + access_token,
                content_type= "application/json"
            ))
        self.assertEqual(200, checkout.status_code)

    def test_member_checkout(self):
        # a member shouldn't be able to checkout 
        family = self.app.post('/family/register', data=json.dumps(self.family_info))
        self.assertEqual(201, family.status_code)
        family_data = json.loads(family.data.decode())

        self.member_info["invite_code"] = family_data['response']['member']
        member = self.app.post('/member/register', data=json.dumps(self.member_info))
        self.assertEqual(201, member.status_code)

        token = self.app.post('/signin', data=json.dumps({"email":self.member_info["email"], "password":self.member_info["password"]}))
        self.assertEqual(200, token.status_code)
        access_token = json.loads(token.data.decode())['token']

        checkout = self.app.post('/checkout', 
        data=json.dumps(self.checkout_info), 
        headers=dict(
                Authorization="Bearer " + access_token,
                content_type= "application/json"
            ))
        self.assertEqual(403, checkout.status_code)

