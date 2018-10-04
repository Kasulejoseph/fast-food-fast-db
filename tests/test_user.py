from app.models.model import User
from tests.test_base import BaseTestCase
from app.database.connect import Database
import json
db = Database()


class TestAuth(BaseTestCase):

    def test_user_class(self):
        user = User(1, "KASULE", "kasule@gmail.com", "kansanga", 1234, 'user')
        self.assertTrue(user)

    def test_details_json_format(self):
        with self.client:
            result = self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "1234", "user")
            self.assertTrue(result.content_type == "application/json")

    def test_email_not_valid(self):
        """
         Test for invalid email address
         """
        register = {
            "username": "kasule",
            "email": "email",
            "location": "location",
            "password": "password",
            "role": "user"
        }
        rs = self.client.post(
            '/api/v1/auth/signup',
            content_type="application/json",
            data=json.dumps(register)
            )
        data = json.loads(rs.data.decode())
        self.assertEqual(rs.status_code, 202)
        self.assertTrue(data['status'] == 'Error')
        self.assertTrue(data['message'] == 'Missing or wrong email format')

    def test_short_password(self):
        """
        Test for short password
        """
        with self.client:
            result = self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "124", "user")
            self.assertEqual(result.status_code, 202)
            data = json.loads(result.data.decode())
            self.assertTrue(data['status'] == 'Failed')
            self.assertTrue(data['message'] == 'Ensure password is morethan 4 characters')

    def test_username_is_string(self):
        """
        Test username isstring
        """
        with self.client:
            result = self.signup_user(
                1234, "kasule@gmail.com", "kansanga", "1246575", "user")
            self.assertEqual(result.status_code, 202)
            data = json.loads(result.data.decode())
            self.assertTrue(data['status'] == 'Type Error')
            self.assertTrue(data['message'] == 'username must all be string')

    def test_spaces_in_username(self):
        """
        Test username has no spaces between characters
        """
        with self.client:
            result = self.signup_user(
                "     ", "kasule@gmail.com", "kansanga", "1246575", "user")
            self.assertEqual(result.status_code, 400)
            data = json.loads(result.data.decode())
            self.assertTrue(data['status'] == 'Space Error')
            self.assertTrue(data['message'] == 'Username should not have space, better user -')
  
    def test_username_not_provided(self):
        """
        Test username field left empty
        """
        with self.client:
            result = self.signup_user(
                "", "kasule@gmail.com", "kansanga", "1246575", "user")
            self.assertEqual(result.status_code, 400)
            data = json.loads(result.data.decode())
            self.assertTrue(data['status'] == 'Missing')
            self.assertTrue(data['message'] == 'Username required')

    def test_user_dat_not_json(self):
        """
        Test Content_type not application/json for sign up request
        """
        rv = self.client.post(
            '/api/v1/auth/signup',
            content_type="text",
            data=json.dumps(dict({'status': 'register'}))
        )
        self.assertEqual(rv.status_code, 202)
        self.assertIn('"message": "Content-type must be in json"', str(rv.data))

    def test_content_type_4_login_not_json(self):
        """
        Test Content_type not application/json for login request
        """
        rv = self.client.post(
            '/api/v1/auth/login',
            content_type="text",
            data=json.dumps(dict({'status': 'register'}))
        )
        self.assertEqual(rv.status_code, 202)
        self.assertIn('"message": "Content-type must be in json"', str(rv.data))

    def test_user_already_exist(self):
        with self.client:
            self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "123464", "user")
            result = self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "123464", "user")
            self.assertEqual(result.status_code, 409)
            data = json.loads(result.data.decode())
            self.assertTrue(data['status'] == 'Failed')
            self.assertTrue(data['message'] == 'User already registered')

    def test_successful_login(self):
        with self.client:
            self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "12389894", "user")
            response = self.login_user("kasule", "12389894")
            res = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(res['username'] == 'kasule')
            self.assertEqual(
                "You have succesfully logged in.", str(res['message']))
            self.assertTrue(res['auth_token'])

    def test_login_credentials(self):
        with self.client:
            self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "12389894", "user")
            resp = self.login_user("kasule", "boooooooo")
            res = json.loads(resp.data.decode())
            self.assertEqual(resp.status_code, 401)
            self.assertTrue(res['status'] == 'Failed')
            self.assertEqual(
                'incorrect password', str(res['message']))

    def test_successful_signup(self):
        with self.client:
            result = self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "12347809", "admin")
            self.assertEqual(result.status_code, 201)
            res = json.loads(result.data.decode())
            self.assertTrue(res['status'] == 'Success')
            self.assertEqual(
                'User account successfully created, log in',
                str(res['message']))
                
                