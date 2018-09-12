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

    list_info_2 = {
        "alias": "cats2",
        "in_store": "Walmart"
    }

    invalid_cart_info = {
        "alias": "cat_alias",
        "in_cart": True,
        "in_store": "Walmart",
        "item_name": "cat",
        "item_image": "https://images.huffingtonpost.com/2016-05-30-1464600256-1952992-cutecatnames-thumb.jpg",
        "item_price": 1200,
        "item_quantity": 24,
        "list_to_cart_id": 3,
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

    list_info_2_edit = {
        "alias": "edit cat",
        "in_cart": False,
        "in_store": "Walmart",
        "item_name": "cat2",
        "item_image": "https://images.huffingtonpost.com/2016-05-30-1464600256-1952992-cutecatnames-thumb.jpg",
        "item_price": 1200,
        "item_quantity": 24,
        "list_to_cart_id": 2,
    }

    cart_info_2_edit = {
        "alias": "edit cat",
        "in_cart": True,
        "in_store": "Walmart",
        "item_name": "cat2",
        "item_image": "https://images.huffingtonpost.com/2016-05-30-1464600256-1952992-cutecatnames-thumb.jpg",
        "item_price": 1200,
        "item_quantity": 24,
        "list_to_cart_id": 2,
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
    
    def test_list_CRUD(self):
        # both admin and member should be able to add item to the list.
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
        ### setup till here
        # adding to list as admin and member Create check
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
        # getting from list as admin and member Get check
        list_by_admin = self.app.get('/listtocart/list',
        headers=dict(
            Authorization="Bearer " + admin_token,
            content_type= "application/json"
        ))
        self.assertEqual(200, list_by_admin.status_code)
        list_get_data_admin = json.loads(list_by_admin.data.decode())

        list_by_member = self.app.get('/listtocart/list',
        headers=dict(
            Authorization="Bearer " + member_token,
            content_type= "application/json"
        ))
        self.assertEqual(200, list_by_member.status_code)
        list_get_data_member = json.loads(list_by_member.data.decode())

        self.assertEqual(Helper.ordered(list_get_data_admin), Helper.ordered(list_get_data_member))
        self.assertEqual(2, len(list_get_data_admin['response']))

        # delete an item from list 
        # delete invalid list to cart obj
        delete_from_list = self.app.delete('/listtocart', 
        data=json.dumps({"list_to_cart_id": 3}), 
        headers=dict(
                Authorization="Bearer " + member_token,
                content_type= "application/json"
            ))
        self.assertEqual(400, delete_from_list.status_code)
        list_by_admin = self.app.get('/listtocart/list',
        headers=dict(
            Authorization="Bearer " + admin_token,
            content_type= "application/json"
        ))
        self.assertEqual(200, list_by_admin.status_code)
        list_get_data_admin = json.loads(list_by_admin.data.decode())
        self.assertEqual(2, len(list_get_data_admin['response']))
        # valid delete
        delete_from_list = self.app.delete('/listtocart', 
        data=json.dumps({"list_to_cart_id": 1}), 
        headers=dict(
                Authorization="Bearer " + member_token,
                content_type= "application/json"
            ))
        self.assertEqual(200, delete_from_list.status_code)
        list_by_admin = self.app.get('/listtocart/list',
        headers=dict(
            Authorization="Bearer " + admin_token,
            content_type= "application/json"
        ))
        self.assertEqual(200, list_by_admin.status_code)
        list_get_data_admin = json.loads(list_by_admin.data.decode())
        self.assertEqual(1, len(list_get_data_admin['response']))
        self.assertEqual(2, list_get_data_admin['response'][0]['id'])

        # edit an item from list 
        # edit invalid list to cart obj 
        invalid_edit_from_list = self.app.put('/listtocart', 
        data=json.dumps(self.cart_info_1), 
        headers=dict(
                Authorization="Bearer " + member_token,
                content_type= "application/json"
            ))
        self.assertEqual(400, invalid_edit_from_list.status_code)
        # valid edit
        edit_from_list = self.app.put('/listtocart', 
        data=json.dumps(self.list_info_2_edit), 
        headers=dict(
                Authorization="Bearer " + member_token,
                content_type= "application/json"
            ))
        self.assertEqual(200, edit_from_list.status_code)
        list_by_admin = self.app.get('/listtocart/list',
        headers=dict(
            Authorization="Bearer " + admin_token,
            content_type= "application/json"
        ))
        self.assertEqual(200, list_by_admin.status_code)
        list_get_data_admin = json.loads(list_by_admin.data.decode())
        self.assertEqual(1, len(list_get_data_admin['response']))
        self.assertEqual("edit cat", list_get_data_admin['response'][0]['alias'])

        # valid edit 2
        edit_from_list = self.app.put('/listtocart', 
        data=json.dumps(self.cart_info_2_edit), 
        headers=dict(
                Authorization="Bearer " + member_token,
                content_type= "application/json"
            ))
        self.assertEqual(200, edit_from_list.status_code)
        list_by_admin = self.app.get('/listtocart/list',
        headers=dict(
            Authorization="Bearer " + admin_token,
            content_type= "application/json"
        ))
        self.assertEqual(200, list_by_admin.status_code)
        list_get_data_admin = json.loads(list_by_admin.data.decode())
        self.assertEqual(0, len(list_get_data_admin['response']))



    def test_cart_CRUD(self):
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
        # switch 2 items to cart
        member_add_to_cart = self.app.post('/listtocart',
        data=json.dumps({"list_to_cart_id": 1}),
        headers=dict(
            Authorization="Bearer " + member_token,
            content_type="application/json"
        ))
        self.assertEqual(200, member_add_to_cart.status_code)

        admin_add_to_cart = self.app.post('/listtocart',
        data=json.dumps({"list_to_cart_id": 2}),
        headers=dict(
            Authorization="Bearer " + admin_token,
            content_type="application/json"
        ))
        self.assertEqual(200, admin_add_to_cart.status_code)

        # getting empty list as admin and member
        list_by_member = self.app.get('/listtocart/list',
        headers=dict(
            Authorization="Bearer " + member_token,
            content_type= "application/json"
        ))
        self.assertEqual(200, list_by_member.status_code)
        list_get_data_member = json.loads(list_by_member.data.decode())
        self.assertEqual(0, len(list_get_data_member['response']))

        # getting cart length of 2 as admin and member
        cart_by_member = self.app.get('/listtocart/cart',
        headers=dict(
            Authorization="Bearer " + member_token,
            content_type= "application/json"
        ))
        self.assertEqual(200, cart_by_member.status_code)
        cart_get_data_member = json.loads(cart_by_member.data.decode())
        cart_by_admin = self.app.get('/listtocart/cart',
        headers=dict(
            Authorization="Bearer " + admin_token,
            content_type= "application/json"
        ))
        self.assertEqual(200, cart_by_admin.status_code)
        cart_get_data_admin = json.loads(cart_by_admin.data.decode())

        self.assertEqual(Helper.ordered(cart_get_data_admin), Helper.ordered(cart_get_data_member))
        self.assertEqual(2, len(cart_get_data_admin['response']))

        # back to list
        admin_add_to_cart = self.app.post('/listtocart',
        data=json.dumps({"list_to_cart_id": 2}),
        headers=dict(
            Authorization="Bearer " + admin_token,
            content_type="application/json"
        ))
        self.assertEqual(200, admin_add_to_cart.status_code)
        cart_by_member = self.app.get('/listtocart/cart',
        headers=dict(
            Authorization="Bearer " + member_token,
            content_type= "application/json"
        ))
        self.assertEqual(200, cart_by_member.status_code)
        cart_get_data_member = json.loads(cart_by_member.data.decode())
        self.assertEqual(1, len(cart_get_data_member))
