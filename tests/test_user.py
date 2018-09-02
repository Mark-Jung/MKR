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

    initial_member_info = {
        "email": "niche@niche.io",
        "first_name": "niche",
        "last_name": "nichel",
        "authority": 1,
        "password": "nicho"
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

    def test_family_creation(self):

        family = self.app.post('/family/register', data=json.dumps(self.family_info))
        self.assertEqual(201, family.status_code)
        family_data = json.loads(family.data.decode())
        print(family_data)

    def test_member_creation(self):

        family = self.app.post('/family/register', data=json.dumps(self.family_info))
        self.assertEqual(201, family.status_code)
        family_data = json.loads(family.data.decode())
        print(family_data)

        # self.member_info["family_id"] = 
        member = self.app.post('/member/register', data=json.dumps(self.member_info))
        self.assertEqual(201, member.status_code)

