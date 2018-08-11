import os, sys
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
basedir = os.path.abspath(os.path.dirname(__file__))
from app import app, socketio
from db import db
import json
from datetime import datetime, timedelta
from flask_socketio import SocketIOTestClient

from helper import Helper

TEST_DB = 'test.db'

class DeviceTests(unittest.TestCase):

    shadow_cash = {
        "device_id": "cash",
        "shadow_metadata": {
            "percent": 0
        },
        "alert_level": 23,
        "container": 1,
        "alias": "monay"
    }

    shadow_money = {
        "device_id": "money",
        "shadow_metadata": {
            "percent": 0
        },
        "alert_level": 23,
        "container": 1,
        "alias": "monaaaaaaay"
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
        self.socketio = SocketIOTestClient(app, socketio)
        self.app = app.test_client()
        db.init_app(app)
        db.drop_all(app=app)
        db.create_all(app=app)


    # executed after each test
    def tearDown(self):
        pass

    def test_socketio_on_create(self):
        self.socketio.emit("create")
        events = self.socketio.get_received()
        self.assertEqual("update", events[0]["name"])
    
    def test_socketio_on_update(self):
        sample_niche1 = self.app.post('/device/register', data=json.dumps(self.shadow_cash))
        self.assertEqual(201, sample_niche1.status_code)
        sample_niche2 = self.app.post('/device/register', data=json.dumps(self.shadow_money))
        self.assertEqual(201, sample_niche2.status_code)
        sample_stamp = self.app.post('/device', data=json.dumps({"device_id": "cash", "metadata":{"battery": 23, "percentage": 12 }}))
        self.assertEqual(201, sample_stamp.status_code)

        self.socketio.emit("update", ["cash"])
        events = self.socketio.get_received()
        self.assertEqual("updated", events[1]["name"])

        result = events[1]["args"][0][0]
        self.assertEqual("cash", events[1]["args"][0][0]['device_id'])

    def test_socketio_on_update_error(self):
        sample_niche1 = self.app.post('/device/register', data=json.dumps(self.shadow_cash))
        self.assertEqual(201, sample_niche1.status_code)
        sample_niche2 = self.app.post('/device/register', data=json.dumps(self.shadow_money))
        self.assertEqual(201, sample_niche2.status_code)
        sample_stamp = self.app.post('/device', data=json.dumps({"device_id": "cash", "metadata":{"battery": 23, "percentage": 12 }}))
        self.assertEqual(201, sample_stamp.status_code)

        self.socketio.emit("update", ["umur"])
        events = self.socketio.get_received()
        self.assertEqual("error", events[1]["name"])
