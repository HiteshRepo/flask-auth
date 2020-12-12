import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    'username', type=str, required=True, help='This field cannot be left blank')
_user_parser.add_argument(
    'password', type=str, required=True, help='This field cannot be left blank')


class UserRegister(Resource):

    def post(self):
        pass


class User(Resource):
    pass


class UserLogin(Resource):
    pass


class UserLogout(Resource):
    pass


class UserList(Resource):
    def get(self):
        # return {'users': list(map(lambda x: x.json(), UserModel.find_all()))}
        return {'users': [{'name': 'Hitesh1', 'age': 26}, {'name': 'Hitesh2', 'age': 27}]}
