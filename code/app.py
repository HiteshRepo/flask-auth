from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from datetime import timedelta
import sqlite3

from resources.user import UserRegister, User, UserLogin, UserLogout, UserList
from blacklist import BLACKLIST

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'api-key'

api = Api(app)

app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=300)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'Token has been revoked.',
        'error': 'token_revoked'
    }), 401


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401


api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserList, '/')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000)
