import unittest
import json
from app import create_app
from db import db


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

    def test_user_name_error(self):
        self.creation_payload['username'] = 'hitesh 12345678'
        res = self.client().post('http://localhost:5000/register', data=self.creation_payload)
        self.assertEqual(res.status_code, 400)
        res = json.loads(res.data)
        self.assertIn(
            'username should be max 8 characters long and should have at least 1 character', str(res['message']))

    def test_password_error(self):
        self.creation_payload['password'] = 'pass%1@'
        res = self.client().post('http://localhost:5000/register', data=self.creation_payload)
        self.assertEqual(res.status_code, 400)
        res = json.loads(res.data)
        self.assertIn(
            'Password must contain at least one character, one number and any one of these (underscore, hyphen, hash) and Password max length should be 6', str(res['message']))

    def test_email_error(self):
        self.creation_payload['email'] = 'hitesh@gmailcom'
        res = self.client().post('http://localhost:5000/register', data=self.creation_payload)
        self.assertEqual(res.status_code, 400)
        res = json.loads(res.data)
        print(res)
        self.assertIn(
            'Email should have @ and .', str(res['message']))

    def test_phonenum_error(self):
        self.creation_payload['phonenum'] = '987'
        res = self.client().post('http://localhost:5000/register', data=self.creation_payload)
        self.assertEqual(res.status_code, 400)
        res = json.loads(res.data)
        print(res)
        self.assertIn(
            'Phone Number must be a valid Indian Cell phone number', str(res['message']))

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
