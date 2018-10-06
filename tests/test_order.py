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
            headers=dict(Authorization='Bearer' " " + token)
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
                headers=dict(Authorization='Bearer' " " + token)
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
                headers=dict(Authorization='Bearer' " " + token)
            )
            data = json.loads(result.data.decode())
            self.assertIn(
                'no orders posted yet', str(data))
            self.assertEqual(result.status_code, 404)

    def test_no_order_in_get_all(self):
        with self.client:
            all = Database().get_all_orders()
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
                headers=dict(Authorization='Bearer' " " + token),
                data=json.dumps(all)
            )
            da = json.loads(result.data.decode())
            self.assertIn("no orders posted yet", str(result.data))
            self.assertEqual(result.status_code, 404)

    def test_user_order_request_not_in_json(self):
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
            result = self.client.post(
                '/api/v1/users/orders/',
                headers=dict(Authorization='Bearer' " " + token),
                content_type="text/javascript"
            )
            data = json.loads(result.data.decode())
            self.assertEqual(result.status_code, 401)
            self.assertEqual(
                data['message'], 'Content type must be application/json')

    def test_meal_id_not_integer(self):
        with self.client:
            self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "12389894", "admin")
            response = self.login_user("kasule", "12389894")
            res = json.loads(response.data.decode())
            self.assertTrue(res['auth_token'])
            token = res['auth_token']
            result = self.client.post(
                '/api/v1/users/orders/',
                headers=dict(Authorization='Bearer' " " + token),
                content_type="application/json",
                data=json.dumps({'meal_id': 'string'})
            )
            data = json.loads(result.data.decode())
            self.assertEqual(result.status_code, 401)
            self.assertEqual(
                data['message'], 'menu ids should be of integer data types only')

    def test_menu_id_is_zero(self):
        with self.client:
            self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "12389894", "admin")
            response = self.login_user("kasule", "12389894")
            res = json.loads(response.data.decode())
            self.assertTrue(res['auth_token'])
            token = res['auth_token']
            result = self.client.post(
                '/api/v1/users/orders/',
                headers=dict(Authorization='Bearer' " " + token),
                content_type="application/json",
                data=json.dumps({'meal_id': 0})
            )
            data = json.loads(result.data.decode())
            self.assertEqual(result.status_code, 401)
            self.assertEqual(
                data['message'], 'Zero is not a menu id')

    def test_no_food_item_on_menu_for_the_id_used(self):
        with self.client:
            self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "12389894", "admin")
            response = self.login_user("kasule", "12389894")
            res = json.loads(response.data.decode())
            self.assertTrue(res['auth_token'])
            token = res['auth_token']
            result = self.client.post(
                '/api/v1/users/orders/',
                headers=dict(Authorization='Bearer' " " + token),
                content_type="application/json",
                data=json.dumps({'meal_id': 2})
            )
            id_menu = 2
            Database().get_order_by_value('menu', 'menu_id', id_menu)
            data = json.loads(result.data.decode())
            self.assertEqual(result.status_code, 404)
            self.assertIn("No item for that id", str(data))

    def test_menu_item_created(self):
        item = {
            "meal": "katogo",
            "description": "all",
            "price": 2000
        }
        Database().add_to_menu(item['meal'], item['description'], item['price'])
        result = self.client.post(
                '/api/v1/menu',
                content_type="application/json",
                data=json.dumps(item)
            )
        data = json.loads(result.data.decode())
        self.assertEqual(result.status_code, 201)
        self.assertIn('successfully added to menu', str(data))

    def test_user_successfull_create_an_order(self):
        with self.client:
            self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "12389894", "admin")
            response = self.login_user("kasule", "12389894")
            res = json.loads(response.data.decode())
            self.assertTrue(res['auth_token'])
            token = res['auth_token']
            Database().add_to_menu("katogo", "all kind", 6000)

            result = self.client.post(
                '/api/v1/users/orders/',
                headers=dict(Authorization='Bearer' " " + token),
                content_type="application/json",
                data=json.dumps({'meal_id': 1})
            )
            id_menu = 1
            Database().get_order_by_value('menu', 'menu_id', id_menu)
            data = json.loads(result.data.decode())
            self.assertEqual(result.status_code, 200)
            self.assertEqual(data['message'], 'Order successfully submited')
            self.assertEqual(data['status'], 'Success')




