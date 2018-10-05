from app.views.orders import OrderAll, OrderPost, OrderById, UpdateStatus
from tests.test_base import BaseTestCase
from app.database.connect import Database
import json
db = Database()


class TestOrder(BaseTestCase):

    def test_use_a_token_from_a_friend(self):
        """
        The method verifies a valid user or sniffers
        """
        token = """eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Imthc3VsZTAwMDAwMDBqb3NlcEBnbWFpbC5jb20iLCJyb2xlIjoidXNlciIsImlhdCI6MTUzODY2NzU2OSwiZXhwIjoxNTQzODUxNTY5LCJzdWIiOjF9.6xtUvM3ULJWuPq2Nd8yPfBwZGfX1s7GzMXA5pZWx_OU"""
        res = self.client.get(
            '/api/v1/orders/',
            headers = dict(Authorization='Bearer' " " + token)
        )
        data = json.loads(res.data.decode())
        self.assertTrue(data['message'], 'User not loged in')
        self.assertEqual(res.status_code, 400)

    def test_user_cant_access_admin_route(self):
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
            token = res['auth_token']
            result = self.client.get(
                '/api/v1/orders/',
                headers = dict(Authorization='Bearer' " " + token)
            )
            data = json.loads(result.data.decode())
            self.assertIn(
                'You dont have permission to access this route', str(data))
            self.assertEqual(result.status_code, 409)
    
    def test_admin_can_access_get_all_order_route(self):
        with self.client:
            self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "12389894", "admin")
            response = self.login_user("kasule", "12389894")
            res = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(res['username'] == 'kasule')
            self.assertEqual(
                "You have succesfully logged in.", str(res['message']))
            self.assertTrue(res['auth_token'])
            token = res['auth_token']
            result = self.client.get(
                '/api/v1/orders/',
                headers = dict(Authorization='Bearer' " " + token)
            )
            data = json.loads(result.data.decode())
            self.assertIn(
                'no orders posted yet', str(data))
            self.assertEqual(result.status_code, 404)



