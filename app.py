import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_heroku import Heroku

app = Flask(__name__)
#api = Api(app)

"""
DB_STRING = f'postgresql://{os.environ.get("DATABASE_USER", 3)}:{os.environ.get("DATABASE_PASS", 3)}@{os.environ.get("DB_HOST", 3)}/{os.environ.get("DB_NAME", 3)}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DB_STRING
db = SQLAlchemy(app)
"""
"""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

is_deployed = os.environ.get("IS_DEPLOYED", "")

if not is_deployed:
    print('Using Localhost Database')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SECRET_KEY'] = os.environ.get("APP_SECRET", 3)
    db = SQLAlchemy(app)
else:
    print("Using Cloud Database")
    heroku = Heroku(app)
    db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET", 3)
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)

import views, models, resources

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')
"""
@app.route("/")
def home_view():
        return "<h1>APP RUNNING</h1>"





if __name__ == ' __main__':
    app.run()