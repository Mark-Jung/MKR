from db import db
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
import jwt

from models.basemodel import BaseModel
from utils.jsonable import JsonEncodedDict

class MemberModel(db.Model, BaseModel):
    __tablename__ = "member"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)

    email = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    fam_id = db.Column(db.Integer, db.ForeignKey('family.id'))
    authority = db.Column(db.Integer)
    password = db.Column(db.String(255))


    def __init__(self, first_name, last_name, email, fam_id, authority, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.fam_id = fam_id
        self.authority = authority
        self.password = Bcrypt().generate_password_hash(password).decode()

    def json(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "fam_id": self.fam_id,
            "authority": self.authority,
        }
        
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_family(cls, fam_id):
        return cls.query.filter_by(fam_id=fam_id).all()

    def validate_password(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return Bcrypt().check_password_hash(self.password, password)
    
    def generate_token(self):
        """ Generates the access token"""
        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(days=100),
                'iat': datetime.utcnow(),
                'sub': self._id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_bytes = jwt.encode(
                payload,
                #'wjdrngusisthecreatorofreedforfun',
                os.environ['SECRET'],
                algorithm='HS256'
            )
            return jwt_bytes
        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def update_token(token):
        """
        Decodes the access token and if the expiration date is within 14 days,
        give them a 100 day extension
        """
        try:
            payload = jwt.decode(token, os.environ['SECRET'])
            payload['exp'] = datetime.utcnow() + timedelta(days=100)
            jwt_bytes = jwt.encode(
                    payload,
                    os.environ['SECRET'],
                    algorithm='HS256'
                    )
            return jwt_bytes
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, os.environ['SECRET'])
            return "", payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token", None
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login", None
