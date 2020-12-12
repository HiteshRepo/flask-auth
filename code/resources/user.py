import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
import re
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    'username', type=str, required=True, help='This field cannot be left blank')
_user_parser.add_argument(
    'password', type=str, required=True, help='This field cannot be left blank')
_user_parser.add_argument(
    'email', type=str, required=True, help='This field cannot be left blank')
_user_parser.add_argument(
    'phonenum', type=str, required=True, help='This field cannot be left blank')


class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'username already taken, so not available'}, 422

        if not self.validateUserName(data['username']):
            return {'message': 'username should be max 8 characters long and should have at least 1 character'}, 400

        if not self.validatePassword(data['password']):
            return {'message': 'Password must contain at least one character, one number and any one of these (underscore, hyphen, hash) and Password max length should be 6'}, 400

        if not self.validateEmail(data['email']):
            return {'message': 'Email should have @ and .'}, 400

        if not self.validatePhoneNum(data['phonenum']):
            return {'message': 'Phone Number must be a valid Indian Cell phone number'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'user created successfully'}, 201

    def validateUserName(self, username):
        return len(username) <= 8 and len(username) > 0

    def validatePassword(self, password):
        if re.fullmatch(r'[A-Za-z0-9_-#]{1,}', password) and len(password) <= 6:
            return True
        return False

    def validateEmail(self, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False
        return True

    def validatePhoneNum(self, phonenum):
        return len(phonenum) == 10


class User(Resource):
    pass


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            return {
                'access_token': access_token
            }, 200
        return {'message': 'Invalid credentials'}, 401


class UserLogout(Resource):
    pass


class UserList(Resource):
    def get(self):
        # return {'users': list(map(lambda x: x.json(), UserModel.find_all()))}
        return {'users': [{'name': 'Hitesh1', 'age': 26}, {'name': 'Hitesh2', 'age': 27}]}
