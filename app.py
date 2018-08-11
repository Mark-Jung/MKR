import os

from db import db
from flask import Flask, request, redirect, Response
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_basicauth import BasicAuth
from werkzeug.exceptions import HTTPException

from views.DeviceDataView import DeviceDataView 

from models.DeviceDataModel import DeviceDataModel
from models.DeviceShadowModel import DeviceShadowModel


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///localdata.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BASIC_AUTH_USERNAME'] = 'niche'
app.config['BASIC_AUTH_PASSWORD'] = 'selmanisgod'
migrate = Migrate(app, db)
basic_auth = BasicAuth(app)
admin = Admin(app, name="nich", template_mode='bootstrap3')

if __name__ == '__main__':
    CORS(app)
#else:
    # CORS(app, resources={r"/*": {"origins": "idk it yet"}})

@app.route('/')
def hello_world():
    return "running!"

@app.route('/device/register', methods=['POST'])
def create_niche():
    return DeviceDataView.register_device()

@app.route('/device', methods=['GET', 'POST'])
def collect_data():
    if request.method == 'POST':
        return DeviceDataView.collect_data()
    elif request.method == 'GET':
        return DeviceDataView.get_all()

@app.route('/dashboard', methods=['POST'])
def load_dashboard():
    return DeviceDataView.get_niches()

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
    column_list = ['device_id', 'date_created', 'date_updated', 'alert_level', 'container', 'alias', 'shadow_metadata']
    column_searchable_list = ['device_id']
    column_filters = ['device_id', 'date_created', 'date_updated', 'alert_level', 'container', 'alias']
    column_default_sort = ('date_created', True)

admin.add_view(DeviceDataAdminView(DeviceDataModel, db.session))
admin.add_view(DeviceShadowAdminView(DeviceShadowModel, db.session))


if __name__ == '__main__':
    db.init_app(app)
    @app.before_first_request
    def create_tables():
        db.create_all()
    app.run()

