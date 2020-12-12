import unittest
import os
import json
from app import create_app
from db import db
from flask_jwt_extended import get_current_user


class UsersAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.db = db
        self.db.init_app(self.app)
        self.client = self.app.test_client

        self.creation_payload = {
            "username": "hitesh 4",
            "password": "pass2",
            "email": "abcd@defg.com",
            "phonenum": "9876543218"
        }

        self.login_payload = {
            "username": "hitesh 4",
            "password": "pass2"
        }

        self.headers = {'Content-Type': 'application/json'}

        with self.app.app_context():
            self.db.create_all()

    def test_user_creation(self):
        res = self.client().post('http://localhost:5000/register', data=self.creation_payload)
        self.assertEqual(res.status_code, 201)
        res = json.loads(res.data)
        self.assertIn('user created successfully', str(res['message']))

    def test_login_api(self):
        self.client().post('http://localhost:5000/register', data=self.creation_payload)
        res = self.client().post('http://localhost:5000/login', data=self.login_payload)
        self.assertEqual(res.status_code, 200)
        res = json.loads(res.data)
        self.assertEqual(list(res.keys())[0], 'access_token')
        self.assertIsNotNone(res['access_token'])

    def test_profile_api_after_login(self):
        self.client().post('http://localhost:5000/register', data=self.creation_payload)
        res = self.client().post('http://localhost:5000/login', data=self.login_payload)
        res = json.loads(res.data)
        token = res['access_token']
        self.headers.update({'Authorization': 'Bearer ' + token})
        res = self.client().get('http://localhost:5000/user/1',
                                data=self.login_payload, headers=self.headers)
        self.assertEqual(res.status_code, 200)
        res = json.loads(res.data)
        self.assertEqual(res['id'], 1)
        self.assertEqual(res['username'], 'hitesh 4')

    def test_profile_api_after_logout(self):
        self.client().post('http://localhost:5000/register', data=self.creation_payload)
        res = self.client().post('http://localhost:5000/login', data=self.login_payload)
        res = json.loads(res.data)
        token = res['access_token']
        self.headers.update({'Authorization': 'Bearer ' + token})
        res = self.client().post('http://localhost:5000/logout',
                                 data=self.login_payload, headers=self.headers)

        res = self.client().get('http://localhost:5000/user/1',
                                data=self.login_payload, headers=self.headers)
        self.assertEqual(res.status_code, 401)
        res = json.loads(res.data)
        self.assertEqual(res['description'], 'Token has been revoked.')
        self.assertEqual(res['error'], 'token_revoked')

    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()


if __name__ == "__main__":
    unittest.main()
