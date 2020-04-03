import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import urllib.parse as up
import psycopg2

#from constants import APP_SETTINGS, JWT_SECRET
from boto.s3.connection import S3Connection
APP_SETTINGS = os.environ.get("APP_SETTINGS", 3)
JWT_SECRET = os.environ.get("JWT_SECRET", 3)
DB_USER = os.environ.get("DATABASE_USER", 3)
DB_PASS = os.environ.get("DATABASE_PASS", 3)
DB_HOST = os.environ.get("DB_HOST", 3)
DB_PORT = os.environ.get("DB_PORT", 3)
DB_NAME = os.environ.get("DB_NAME", 3)
DB_STRING = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
app = Flask(__name__)
api = Api(app)

#db_setup
"""
app.config.from_object(APP_SETTINGS)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
"""

db = SQLAlchemy.create_engine(DB_STRING, {})

#setup jwt
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = JWT_SECRET
jwt = JWTManager(app)

#enable jwt blacklisting
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)

@app.before_first_request
def create_tables():
    db.create_all()

import views, models, resources

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')



