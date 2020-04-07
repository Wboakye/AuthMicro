import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_heroku import Heroku
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

#initialize db
MONGO_ATLAS_URL = os.environ.get("MONGO_ATLAS_URL", 3)
client = MongoClient(MONGO_ATLAS_URL)
db = client.villagedb

app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET", 3)
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return helpers.RevokedToken.is_jti_blacklisted(jti)

import views, helpers, resources

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/verifyauth')


if __name__ == ' __main__':
    app.run()