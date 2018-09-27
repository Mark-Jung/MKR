import os

from db import db
from flask import Flask, request, redirect, Response
from flask_cors import cross_origin
from flask_migrate import Migrate, MigrateCommand
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_basicauth import BasicAuth
from werkzeug.exceptions import HTTPException

from views.CheckoutView import CheckoutView
from views.DeviceDataView import DeviceDataView 
from views.FamilyView import FamilyView
from views.FeedbackView import FeedbackView
from views.ListToCartView import ListToCartView
from views.MemberView import MemberView
from views.VerificationView import VerificationView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///localdata.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BASIC_AUTH_USERNAME'] = 'niche'
app.config['BASIC_AUTH_PASSWORD'] = 'selmanisgod'
migrate = Migrate(app, db)
basic_auth = BasicAuth(app)
admin = Admin(app, name="niche", template_mode='bootstrap3')

@app.route('/')
@cross_origin()
def hello_world():
    return "running!"

@app.route('/checkout', methods=['POST'])
def checkout():
    return CheckoutView.checkout()

@app.route('/device/register', methods=['POST'])
def create_niche():
    return DeviceDataView.register_device()

@app.route('/device', methods=['POST'])
def collect_data():
    return DeviceDataView.collect_data()

@app.route('/dashboard', methods=['GET'])
def load_dashboard():
    return DeviceDataView.get_niches()

@app.route('/family/register', methods=['POST'])
def register_family():
    return FamilyView.register_family()

@app.route('/family/join', methods=['POST'])
def join_family():
    return FamilyView.join_family()

@app.route('/feedback', methods=['POST'])
def respond_feedback():
    return FeedbackView.respond_feedback()

@app.route('/feedback/save', methods=['POST'])
def save_feedback():
    return FeedbackView.save_feedback()

@app.route('/invite', methods=['POST'])
def invite():
    return FamilyView.invite_by_email()

@app.route('/listtocart', methods=['DELETE', 'POST', 'PUT'])
def list_to_cart():
    if request.method == 'DELETE':
        return ListToCartView.delete_list_to_cart()
    elif request.method == 'POST':
        return ListToCartView.switch_list_to_cart()
    elif request.method == 'PUT':
        return ListToCartView.edit_list_to_cart()

@app.route('/listtocart/list', methods=['GET', 'POST'])
def list_to_cart_list():
    if request.method == 'GET':
        return ListToCartView.get_list()
    elif request.method == 'POST':
        return ListToCartView.register_list_to_cart()

@app.route('/listtocart/cart', methods=['GET'])
def list_to_cart_cart():
    if request.method == 'GET':
        return ListToCartView.get_cart()

@app.route('/member/register', methods=['POST'])
def register_member():
    return MemberView.register_member()

@app.route('/niche', methods=['POST', 'PUT'])
def user_niche_actions():
    if request.method == 'POST':
        return DeviceDataView.claim_niche()
    elif request.method == 'PUT':
        return DeviceDataView.edit_niche()

@app.route('/signin', methods=['POST'])
def signin():
    return MemberView.signin()

@app.route('/signin/token', methods=['GET'])
def signin_by_token():
    return MemberView.signin_by_token()

@app.route('/verify', methods=['POST'])
def verify():
    return VerificationView.verify_member()

@app.route('/verify/re', methods=['GET'])
def re_verify():
    return VerificationView.resend_verification()

"""
Admin View imports and definitions
"""
# Model Imports
from models.CheckoutModel import CheckoutModel
from models.DeviceDataModel import DeviceDataModel
from models.DeviceShadowModel import DeviceShadowModel
from models.FamilyModel import FamilyModel
from models.FeedbackModel import FeedbackModel
from models.ListToCartModel import ListToCartModel
from models.MemberModel import MemberModel
from models.ProductModel import ProductModel
from models.VerificationModel import VerificationModel

class ModelView(sqla.ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True
    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))

class DeviceDataAdminView(ModelView):
    column_list = ['id', 'device_id', 'date_created', 'device_metadata']
    column_searchable_list = ['device_id']
    column_filters = ['device_id', 'id', 'date_created']
    column_default_sort = ('date_created', True)

class DeviceShadowAdminView(ModelView):
    column_list = ['fam_id', 'device_id', 'date_created', 'date_updated', 'alert_level', 'container', 'alias', 'shadow_metadata', 'product_metadata']
    column_searchable_list = ['device_id', 'alert_level']
    column_filters = ['fam_id', 'device_id', 'date_created', 'date_updated', 'alert_level', 'container', 'alias']
    column_default_sort = ('fam_id', True)

class CheckoutAdminView(ModelView):
    column_list = ['id', 'date_created', 'total', 'member_id']
    column_filters = ['id', 'date_created', 'total', 'member_id']
    column_default_sort = ('id', True)

class FamilyAdminView(ModelView):
    column_list = ['id', 'date_created', 'address_line1', 'address_line2', 'city', 'state','zip_code', 'name', 'phone', 'email', 'admin_invite', 'member_invite']
    column_filters = ['id', 'email', 'name', 'phone', 'admin_invite', 'member_invite']
    column_default_sort = ('id', True)

class FeedbackAdminView(ModelView):
    column_list = ['id', 'date_created', 'feedback_url', 'feedback_duration', 'transcription_url', 'member_id']
    column_filters = ['id', 'date_created', 'feedback_url', 'feedback_duration', 'transcription_url', 'member_id']
    column_default_sort = ('id', True) 

class ListToCartAdminView(ModelView):
    column_list = ['id', 'date_created', 'alias', 'in_cart', 'in_store', 'adder', 'item_name', 'item_image', 'item_price', 'item_rating', 'item_quantity', 'fam_id']
    column_filters = ['id', 'adder', 'alias', 'item_name', 'item_image', 'item_price', 'item_quantity', 'fam_id']
    column_default_sort = ('id', True)

class MemberAdminView(ModelView):
    column_list = ['id', 'date_created', 'email', 'first_name', 'last_name', 'authority', 'verified', 'fam_id', ]
    column_filters = ['id', 'date_created', 'email', 'first_name', 'last_name', 'authority', 'verified', 'fam_id']
    column_default_sort = ('id', True)

class ProductAdminView(ModelView):
    column_list = ['id', 'date_created', 'store', 'price', 'url', 'name', 'checkout_id']
    column_filters = ['id', 'date_created', 'store', 'price', 'url', 'name', 'checkout_id']
    column_default_sort = ('id', True)

class VerificationAdminView(ModelView):
    column_list = ['id', 'date_created', 'value', 'member_id']
    column_filters = ['id', 'date_created', 'value', 'member_id']
    column_default_sort = ('id', True)

admin.add_view(CheckoutAdminView(CheckoutModel, db.session))
admin.add_view(DeviceDataAdminView(DeviceDataModel, db.session))
admin.add_view(DeviceShadowAdminView(DeviceShadowModel, db.session))
admin.add_view(FamilyAdminView(FamilyModel, db.session))
admin.add_view(FeedbackAdminView(FeedbackModel, db.session))
admin.add_view(ListToCartAdminView(ListToCartModel, db.session))
admin.add_view(MemberAdminView(MemberModel, db.session))
admin.add_view(ProductAdminView(ProductModel, db.session))
admin.add_view(VerificationAdminView(VerificationModel, db.session))


if __name__ == '__main__':
    db.init_app(app)
    @app.before_first_request
    def create_tables():
        db.create_all()
    app.run()

