from app.views.orders import OrderAll, OrderPost, OrderById, UpdateStatus
from tests.test_base import BaseTestCase
from app.database.connect import Database
import json
db = Database()


class TestOrder(BaseTestCase):

    def test_use_a_token_from_a_friend(self):
        """
        User with invalid token can't access
        any secure route
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
        """
        Only users whoo signed up with
        admin role can access admin routes
        """
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
        """
        Only admin can get all orders posted by all users
        """
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

    def test_admin_fetch_all_orders_submited_by_users(self):
        """
        All orders submit by different users
        can be fetched by only admin
        """
        with self.client:
            self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "12389894", "admin")
            response = self.login_user("kasule", "12389894")
            res = json.loads(response.data.decode())
            self.assertTrue(res['auth_token'])
            token = res['auth_token']
            Database().add_to_menu("katogo", "all kind", 6000)

            self.client.post(
                '/api/v1/users/orders/',
                headers=dict(Authorization='Bearer' " " + token),
                content_type="application/json",
                data=json.dumps({'meal_id': 1})
            )
            id_menu = 1
            Database().get_order_by_value('menu', 'menu_id', id_menu)

            all = Database().get_all_orders()
            result = self.client.get(
                '/api/v1/orders/',
                headers=dict(Authorization='Bearer' " " + token),
                data=json.dumps(all)
            )
            da = json.loads(result.data.decode())
            self.assertGreater(len(da), 0)
            self.assertIn('Orders', str(result.data))
            self.assertEqual(result.status_code, 200)

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

    def test_user_successfull_make_an_order(self):
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

    def test_nothing_on_menu(self):
        Database().fetch_menu()
        result = self.client.get(
                '/api/v1/menu',
                content_type="application/json"
            )
        data = json.loads(result.data.decode())
        self.assertEqual(result.status_code, 404)
        self.assertIn('nothing on menu today', str(data))

    def test_all_menu_items_fetched_successfully(self):
        item = {
            "meal": "katogo",
            "description": "all",
            "price": 2000
        }
        Database().add_to_menu(item['meal'], item['description'], item['price'])
        Database().fetch_menu()
        result = self.client.get(
                '/api/v1/menu',
                content_type="application/json",
                data=json.dumps(item)
            )
        data = json.loads(result.data.decode())
        self.assertEqual(result.status_code, 200)

    def test_no_order_found_by_id(self):
        """
        Admin trying to get all order requests
        for a order id which does not exist
        """
        with self.client:
            self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "12389894", "admin")
            response = self.login_user("kasule", "12389894")
            res = json.loads(response.data.decode())
            self.assertTrue(res['auth_token'])
            token = res['auth_token']
            Database().get_order_by_value('orders', 'order_id', 1)

            result = self.client.get(
                '/api/v1/orders/1',
                headers=dict(Authorization='Bearer' " " + token),
                content_type="application/json"
            )
            data = json.loads(result.data.decode())
            self.assertEqual(result.status_code, 404)
            self.assertEqual(data['status'], 'Failed')
            self.assertTrue(data['message'] == 'No order by that Id')

    def test_admin_get_order_request_user_users_by_id(self):
        """
        Test admin can get all users who requested for
        the same food item, In other words he can
        get a food item request with all the
        customers who request for it
        """
        with self.client:
            self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "12389894", "admin")
            response = self.login_user("kasule", "12389894")
            res = json.loads(response.data.decode())
            self.assertTrue(res['auth_token'])
            token = res['auth_token']
            Database().add_to_menu("katogo", "all kind", 6000)

            self.client.post(
                '/api/v1/users/orders/',
                headers=dict(Authorization='Bearer' " " + token),
                content_type="application/json",
                data=json.dumps({'meal_id': 1})
            )
            Database().get_order_by_value('orders', 'order_id', 1)
            result = self.client.get(
                '/api/v1/orders/1',
                headers=dict(Authorization='Bearer' " " + token),
                content_type="application/json"
            )
            data = json.loads(result.data.decode())
            self.assertEqual(result.status_code, 200)
            self.assertEqual(data['BY'], 'admin')
            self.assertIn("'meal': 'katogo'", str(data))




