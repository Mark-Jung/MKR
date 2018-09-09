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

class ListToCartTests(unittest.TestCase):
    
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

    admin_info = {
        "email": "admin@niche.io",
        "first_name": "admin",
        "last_name": "admin",
        "password": "adminoh"
    }

    member_info = {
        "email": "member@niche.io",
        "first_name": "member",
        "last_name": "member",
        "password": "memberoo"
    }

    list_info = {
        "alias": "cat",
        "in_store" : "Walmart"
    }

    cart_info_1 = {
        "in_store": "Walmart",
        "item_name": "cat",
        "item_image": "https://images.huffingtonpost.com/2016-05-30-1464600256-1952992-cutecatnames-thumb.jpg",
        "item_price": "1200",
        "item_quantity": 24,
        "list_to_cart_id": 1,
    }

    cart_info_2 = {
        "in_store": "Walmart",
        "item_name": "cat",
        "item_image": "https://images.huffingtonpost.com/2016-05-30-1464600256-1952992-cutecatnames-thumb.jpg",
        "item_price": "1200",
        "item_quantity": 24,
        "list_to_cart_id": 1,
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
    
    def test_list_register(self):
        # both admin and member should be able to add item to the list.
        family = self.app.post('/family/register', data=json.dumps(self.family_info))
        self.assertEqual(201, family.status_code)
        family_data = json.loads(family.data.decode())

        self.admin_info["invite_code"] = family_data['response']['admin']
        self.member_info["invite_code"] = family_data['response']['member']
        admin = self.app.post('/member/register', data=json.dumps(self.admin_info))
        member = self.app.post('/member/register', data=json.dumps(self.member_info))
        self.assertEqual(201, admin.status_code)
        self.assertEqual(201, member.status_code)

        token = self.app.post('/signin', data=json.dumps({"email":self.member_info["email"], "password":self.member_info["password"]}))
        self.assertEqual(200, token.status_code)
        member_token = json.loads(token.data.decode())['token']

        token = self.app.post('/signin', data=json.dumps({"email":self.admin_info["email"], "password":self.admin_info["password"]}))
        self.assertEqual(200, token.status_code)
        admin_token = json.loads(token.data.decode())['token']
        ### setup till here

        admin_add_to_list = self.app.post('/listtocart/list', 
        data=json.dumps(self.list_info), 
        headers=dict(
                Authorization="Bearer " + admin_token,
                content_type= "application/json"
            ))
        self.assertEqual(201, admin_add_to_list.status_code)

        member_add_to_list = self.app.post('/listtocart/list', 
        data=json.dumps(self.list_info), 
        headers=dict(
                Authorization="Bearer " + member_token,
                content_type= "application/json"
            ))
        self.assertEqual(201, member_add_to_list.status_code)

    def test_cart_register(self):
        family = self.app.post('/family/register', data=json.dumps(self.family_info))
        self.assertEqual(201, family.status_code)
        family_data = json.loads(family.data.decode())

        self.admin_info["invite_code"] = family_data['response']['admin']
        self.member_info["invite_code"] = family_data['response']['member']
        admin = self.app.post('/member/register', data=json.dumps(self.admin_info))
        member = self.app.post('/member/register', data=json.dumps(self.member_info))
        self.assertEqual(201, admin.status_code)
        self.assertEqual(201, member.status_code)

        token = self.app.post('/signin', data=json.dumps({"email":self.member_info["email"], "password":self.member_info["password"]}))
        self.assertEqual(200, token.status_code)
        member_token = json.loads(token.data.decode())['token']

        token = self.app.post('/signin', data=json.dumps({"email":self.admin_info["email"], "password":self.admin_info["password"]}))
        self.assertEqual(200, token.status_code)
        admin_token = json.loads(token.data.decode())['token']

        admin_add_to_list = self.app.post('/listtocart/list', 
        data=json.dumps(self.list_info), 
        headers=dict(
                Authorization="Bearer " + admin_token,
                content_type= "application/json"
            ))
        self.assertEqual(201, admin_add_to_list.status_code)

        member_add_to_list = self.app.post('/listtocart/list', 
        data=json.dumps(self.list_info), 
        headers=dict(
                Authorization="Bearer " + member_token,
                content_type= "application/json"
            ))
        self.assertEqual(201, member_add_to_list.status_code)

        ### setup till here. Created 1 member, 1 admin, 2 list items.
        member_add_to_cart = self.app.post('/listtocart/cart',
        data=json.dumps(self.cart_info_1),
        headers=dict(
            Authorization="Bearer " + member_token,
            content_type="application/json"
        ))
        self.assertEqual(200, member_add_to_cart.status_code)

        admin_add_to_cart = self.app.post('/listtocart/cart',
        data=json.dumps(self.cart_info_2),
        headers=dict(
            Authorization="Bearer " + admin_token,
            content_type="application/json"
        ))
        self.assertEqual(200, admin_add_to_cart.status_code)
