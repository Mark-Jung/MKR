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

class CheckoutTests(unittest.TestCase):
    
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

    member_info1 = {
        "email": "member1@niche.io",
        "first_name": "niche",
        "last_name": "nichel",
        "password": "nicolo"
    }

    list_info = {
        "alias": "cat",
        "in_store" : "Walmart"
    }

    list_info_1 = {
        "alias": "cats1",
        "in_store": "Manual"
    }

    cart_info_1 = {
        "alias": "cat_alias",
        "in_cart": True,
        "in_store": "Walmart",
        "item_name": "cat",
        "item_image": "https://images.huffingtonpost.com/2016-05-30-1464600256-1952992-cutecatnames-thumb.jpg",
        "item_price": 1200,
        "item_quantity": 24,
        "list_to_cart_id": 1,
    }

    cart_info_2 = {
        "alias": "cat_alias2",
        "in_cart": True,
        "in_store": "Walmart",
        "item_name": "cat2",
        "item_image": "https://images.huffingtonpost.com/2016-05-30-1464600256-1952992-cutecatnames-thumb.jpg",
        "item_price": 1200,
        "item_quantity": 24,
        "list_to_cart_id": 2,
    }

    checkout_info = {
        "total": 2400,
        "items": [1, 2]
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

        # add to list
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

        # switch 2 items to cart
        member_add_to_cart = self.app.post('/listtocart',
        data=json.dumps({"list_to_cart_id": 1}),
        headers=dict(
            Authorization="Bearer " + member_token,
            content_type="application/json"
        ))
        self.assertEqual(200, member_add_to_cart.status_code)
        member_add_to_cart = self.app.post('/listtocart',
        data=json.dumps({"list_to_cart_id": 2}),
        headers=dict(
            Authorization="Bearer " + member_token,
            content_type="application/json"
        ))
        self.assertEqual(200, member_add_to_cart.status_code)

        # invalid_checkout - member can't checkout
        checkout = self.app.post('/checkout', 
        data=json.dumps(self.checkout_info), 
        headers=dict(
                Authorization="Bearer " + member_token,
                content_type= "application/json"
            ))
        self.assertEqual(403, checkout.status_code)

        # invalid_checkout - insufficient data
        checkout = self.app.post('/checkout', 
        data=json.dumps(self.checkout_info), 
        headers=dict(
                Authorization="Bearer " + admin_token,
                content_type= "application/json"
            ))
        self.assertEqual(400, checkout.status_code)

        # fill list_to_cart info so it's sufficient for checkout
        checkout = self.app.put('/listtocart', 
        data=json.dumps(self.cart_info_1), 
        headers=dict(
                Authorization="Bearer " + member_token,
                content_type= "application/json"
            ))
        self.assertEqual(200, checkout.status_code)

        checkout = self.app.put('/listtocart', 
        data=json.dumps(self.cart_info_2), 
        headers=dict(
                Authorization="Bearer " + member_token,
                content_type= "application/json"
            ))
        self.assertEqual(200, checkout.status_code)

        checkout = self.app.post('/checkout', 
        data=json.dumps(self.checkout_info), 
        headers=dict(
                Authorization="Bearer " + admin_token,
                content_type= "application/json"
            ))
        self.assertEqual(200, checkout.status_code)
