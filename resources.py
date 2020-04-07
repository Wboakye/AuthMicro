import os
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from helpers import DbMethods, RevokedToken

from app import db

register_parser = reqparse.RequestParser()
register_parser.add_argument('username', help = 'This field cannot be blank', required = True)
register_parser.add_argument('password', help = 'This field cannot be blank', required = True)
register_parser.add_argument('email', help = 'This field cannot be blank', required = True)
register_parser.add_argument('first_name', help = 'This field cannot be blank', required = True)
register_parser.add_argument('last_name', help = 'This field cannot be blank', required = True)

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', help = 'This field cannot be blank', required = True)
login_parser.add_argument('password', help = 'This field cannot be blank', required = True)

pw_parser = reqparse.RequestParser()
pw_parser.add_argument('password', help = 'This field cannot be blank', required = True)

# TODO: add email/name
class UserRegistration(Resource):
    def post(self):
        #parse data
        data = register_parser.parse_args()

        #validate
        if db.villagers.find_one({"username" : data["username"] }):
            return {'message': 'User {} already exists'.format(data['username'])}, 400

        if db.villagers.find_one({"email" : data["email"] }):
            return {'message': 'User {} already exists'.format(data['email'])}, 400

        if "." or "@" not in data["email"]:
            return {'message': 'Email address not valid'},400

        #create new user, standardize data
        new_user = {
            "first_name": data['first_name'].title(),
            "last_name": data['last_name'].title(),
            "email": data['email'].lower(),
            "username" : data['username'].lower(),
            "password" : DbMethods.generate_hash(data['password'])
        }
        try:
            #save to db
            db.villagers.insert_one(new_user)

            #create jwts
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])

            #send success message with jwts
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token            }
        except:
            return {'message': 'Something went wrong'}, 500

class UserLogin(Resource):
    def post(self):
        data = login_parser.parse_args()
        #find user in db
        if "@" in data['username']:
            current_user = db.villagers.find_one({"email": data['username']})
        else:
            current_user = db.villagers.find_one({"username" : data['username']})

        #if user doesn't exist, return error
        if not current_user:
            return {'message': 'Username or Password does not exist.'}, 401

        #if provided password matches hashed db password return success message w/ jwt
        if  not DbMethods.verify_hash(data['password'], current_user.password):
            return {'message': 'Wrong credentials'}, 401
        access_token = create_access_token(identity = data['username'])
        refresh_token = create_refresh_token(identity = data['username'])

        return {
            'message': 'Logged in as {}'.format(current_user.username),
            'access_token': access_token,
            'refresh_token': refresh_token
            }


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    def get(self):
        ADMIN_PASS = os.environ.get("ADMIN_PASS", 3)
        data = pw_parser.parse_args()
        if ADMIN_PASS is not data["password"]:
            return {"data": f"You don't have permission to perform this action"}, 401
        return db.villagers.find({}), 401

    def delete(self):
        admin_pass = os.environ.get("ADMIN_PASS")
        if not admin_pass:
            return {"data" : "Unable to perform action."}, 500
        data = pw_parser.parse_args()
        if admin_pass != data["password"]:
            return {"data": f"You don't have permission to perform this action"}, 401
        return db.villagers.remove({})


class SecretResource(Resource):
    @jwt_required
    def post(self):
        return {'user' : get_jwt_identity()}