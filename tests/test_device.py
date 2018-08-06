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

    def test_device_shadow_creation(self):
        sample_niche = self.app.post('/device/register', data=json.dumps({"device_id": "cash"}))
        self.assertEqual(201, sample_niche.status_code)

    def test_invalid_device_shadow(self):
        bad_niche_id = self.app.post('/device/register', data=json.dumps({"wow":"hi"}))
        self.assertEqual(400, bad_niche_id.status_code)

    def test_device_data_stamp_creation_and_get_all(self):
        sample_niche = self.app.post('/device/register', data=json.dumps({"device_id": "cash"}))
        self.assertEqual(201, sample_niche.status_code)
        sample_niche = self.app.post('/device/register', data=json.dumps({"device_id": "money"}))
        self.assertEqual(201, sample_niche.status_code)

        sample_stamp = self.app.post('/device', data=json.dumps({"device_id": "cash", "metadata":{"battery": 23, "percentage": 12 }}))
        self.assertEqual(201, sample_stamp.status_code)

        all_stamps = self.app.get('/device')
        self.assertEqual(200, all_stamps.status_code)
        all_stamps_data = json.loads(all_stamps.data.decode())
        self.assertEqual(1, len(all_stamps_data['response']))

        sample_stamp = self.app.post('/device', data=json.dumps({"device_id": "cash", "metadata":{"battery": 23, "percentage": 12 }}))
        self.assertEqual(201, sample_stamp.status_code)
        sample_stamp = self.app.post('/device', data=json.dumps({"device_id": "money", "metadata":{"battery": 23, "percentage": 12 }}))
        self.assertEqual(201, sample_stamp.status_code)

        all_stamps = self.app.get('/device')
        self.assertEqual(200, all_stamps.status_code)
        all_stamps_data = json.loads(all_stamps.data.decode())
        self.assertEqual(3, len(all_stamps_data['response']))

