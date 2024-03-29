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

class DeviceTests(unittest.TestCase):

    shadow_factory_init = {
        "device_id": "trial1"
    }
    shadow_factory_init1 = {
        "device_id": "23121"
    }

    shadow_claim = {
        "device_id": "trial1",
        "shadow_metadata": {
            "percent": 0
        },
        "alert_level": 23,
        "container": 1,
        "alias": "monay",
        "auto_order_store": "",
        "product_metadata": {
            "product_name": "cash",
            "product_image": "url",
            "product_quantity": 2,
            "product_price": 23.22
        }
    }
    shadow_claim1 = {
        "device_id": "23121",
        "shadow_metadata": {
            "percent": 0
        },
        "alert_level": 23,
        "container": 1,
        "alias": "monaaaaaaay",
        "auto_order_store": "",
        "product_metadata": {
            "product_name": "money",
            "product_image": "url",
            "product_quantity": 2,
            "product_price": 23.22
        }
    }

    shadow_edit = {
        "device_id": "trial1",
        "shadow_metadata": {
            "percent": 0
        },
        "alert_level": 50,
        "container": 1,
        "alias": "edited shadow",
        "auto_order_store": "",
        "product_metadata": {
            "product_name": "cash",
            "product_image": "url",
            "product_quantity": 2,
            "product_price": 23.22
        }
    }

    shadow_edit1 = {
        "device_id": "23121",
        "shadow_metadata": {
            "percent": 0
        },
        "alert_level": 32,
        "container": 1,
        "alias": "edited shadow1",
        "auto_order_store": "",
        "product_metadata": {
            "product_name": "money",
            "product_image": "url",
            "product_quantity": 2,
            "product_price": 23.22
        }
    }

    family_info = {
        "address_line1": "he",
        "address_line2": "ll",
        "city": "evanston",
        "state": "il",
        "zip_code": 63127,
        "name": "niche",
    }

    family_info_1 = {
        "address_line1": "healthy",
        "address_line2": "ll",
        "city": "evanston",
        "state": "il",
        "zip_code": 63127,
        "name": "niche1",
    }

    member_info = {
        "email": "member@niche.io",
        "phone": "+17365331364",
        "first_name": "member",
        "last_name": "member",
        "password": "nicho"
    }

    member_info_1 = {
        "email": "test@test",
        "phone": "+11234567890",
        "first_name": "membero",
        "last_name": "membero",
        "password": "nichoo"
    }

    shadow_changefam = {
        "secret": "wow",
        "device_id": "trial1",
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

    def test_invalid_device_shadow(self):
        bad_niche_id = self.app.post('/device/register', data=json.dumps({"wow":"hi"}))
        self.assertEqual(400, bad_niche_id.status_code)

    def test_niche_register_claim_stamp(self):

        # create member
        member = self.app.post('/member/register', data=json.dumps(self.member_info))
        admin_token = json.loads(member.data.decode())['token']
        self.assertEqual(201, member.status_code)

        # verify email for member
        verify = self.app.post('/verify',
            data=json.dumps({"verification_code": "test"}),
            headers=dict(
                Authorization="Bearer " + admin_token,
                content_type="application/json"
            ))
        self.assertEqual(200, verify.status_code)

        # create family
        family = self.app.post('/family/register',
            data=json.dumps(self.family_info),
            headers=dict(
                Authorization="Bearer " + admin_token,
                content_type="application/json"
            ))
        self.assertEqual(201, family.status_code)
        family_invite = json.loads(family.data.decode())['response']
        admin_invite = family_invite['admin']
        member_invite = family_invite['member']

        sample_niche = self.app.post('/device/register', data=json.dumps(self.shadow_factory_init))
        self.assertEqual(201, sample_niche.status_code)
        sample_niche = self.app.post('/device/register', data=json.dumps(self.shadow_factory_init1))
        self.assertEqual(201, sample_niche.status_code)
        claimed_niche = self.app.post('/niche', 
            data=json.dumps(self.shadow_claim), 
            headers=dict(
                Authorization="Bearer " + admin_token,
                content_type= "application/json"
            ))
        self.assertEqual(200, claimed_niche.status_code)

        sample_stamp = self.app.post('/device', data=json.dumps({"device_id": "trial1", "metadata":{"battery": 23, "percent": 12 }}))
        Helper.print_error(sample_stamp, 201)
        self.assertEqual(201, sample_stamp.status_code)

        # stamp initially -- case n
        dashboard = self.app.get('/dashboard', headers=dict(
                Authorization="Bearer " + admin_token,
                content_type= "application/json"
            ))
        dashboard_data = json.loads(dashboard.data.decode())
        self.assertEqual(200, dashboard.status_code)
        self.assertEqual(1, len(dashboard_data['response']))
        self.assertEqual(12, dashboard_data['response'][0]['shadow_metadata']['percent'])


        # stamp -- case n + 1
        sample_stamp = self.app.post('/device', data=json.dumps({"device_id": "trial1", "metadata":{"battery": 23, "percent": 23 }}))
        self.assertEqual(201, sample_stamp.status_code)
        dashboard = self.app.get('/dashboard', headers=dict(
                Authorization="Bearer " + admin_token,
                content_type= "application/json"
            )) 
        dashboard_data = json.loads(dashboard.data.decode())
        self.assertEqual(200, dashboard.status_code)
        self.assertEqual(1, len(dashboard_data['response']))
        self.assertEqual(23, dashboard_data['response'][0]['shadow_metadata']['percent'])

        sample_stamp = self.app.post('/device', data=json.dumps({"device_id": "23121", "metadata":{"battery": 23, "percent": 12 }}))
        self.assertEqual(201, sample_stamp.status_code)

        # edit niche_info
        claimed_niche = self.app.put('/niche', 
            data=json.dumps(self.shadow_edit), 
            headers=dict(
                Authorization="Bearer " + admin_token,
                content_type= "application/json"
            ))
        self.assertEqual(200, claimed_niche.status_code)

        dashboard = self.app.get('/dashboard', headers=dict(
                Authorization="Bearer " + admin_token,
                content_type= "application/json"
            )) 
        dashboard_data = json.loads(dashboard.data.decode())
        self.assertEqual(200, dashboard.status_code)
        self.assertEqual(1, len(dashboard_data['response']))
        self.assertEqual("edited shadow", dashboard_data['response'][0]['alias'])

        # create member
        member = self.app.post('/member/register', data=json.dumps(self.member_info_1))
        fam2_token = json.loads(member.data.decode())['token']
        self.assertEqual(201, member.status_code)

        # verify email for member
        verify = self.app.post('/verify',
            data=json.dumps({"verification_code": "test"}),
            headers=dict(
                Authorization="Bearer " + fam2_token,
                content_type="application/json"
            ))
        self.assertEqual(200, verify.status_code)
        # create family
        family = self.app.post('/family/register',
            data=json.dumps(self.family_info_1),
            headers=dict(
                Authorization="Bearer " + fam2_token,
                content_type="application/json"
            ))
        self.assertEqual(201, family.status_code)
        family_invite = json.loads(family.data.decode())['response']
        admin_invite = family_invite['admin']
        member_invite = family_invite['member']

        # change niche_fam
        change_fam = self.app.post('/device/change',
            data=json.dumps(self.shadow_changefam),
            headers=dict(
                Authorization="Bearer " + fam2_token,
                content_type="application/json",
            ))
        self.assertEqual(200, change_fam.status_code)

        dashboard = self.app.get('/dashboard', headers=dict(
                Authorization="Bearer " + fam2_token,
                content_type= "application/json"
            )) 
        dashboard_data = json.loads(dashboard.data.decode())
        self.assertEqual(200, dashboard.status_code)
        self.assertEqual(1, len(dashboard_data['response']))
        self.assertEqual("edited shadow", dashboard_data['response'][0]['alias'])

        dashboard = self.app.get('/dashboard', headers=dict(
                Authorization="Bearer " + admin_token,
                content_type= "application/json"
            )) 
        dashboard_data = json.loads(dashboard.data.decode())
        self.assertEqual(200, dashboard.status_code)
        self.assertEqual(0, len(dashboard_data['response']))

