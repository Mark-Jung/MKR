import os

from db import db
from flask import Flask, request
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from views.DeviceDataView import DeviceDataView 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///localdata.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)
if __name__ == '__main__':
    CORS(app)
#else:
    # CORS(app, resources={r"/*": {"origins": "idk it yet"}})

@app.route('/')
def hello_world():
    return "running!"

@app.route('/device/register', methods=['POST'])
def create_niche():
    if request.method == 'POST':
        return DeviceDataView.register_device()

@app.route('/device', methods=['GET', 'POST'])
def collect_data():
    if request.method == 'POST':
        return DeviceDataView.collect_data()
    elif request.method == 'GET':
        return DeviceDataView.get_all()

if __name__ == '__main__':
    db.init_app(app)
    @app.before_first_request
    def create_tables():
        db.create_all()
    app.run()

