from app.views.orders import OrderAll, OrderPost, OrderById, UpdateStatus
from tests.test_base import BaseTestCase
from app.database.connect import Database
import json
db = Database()


class TestOrder(BaseTestCase):

    def test_menu_in_json(self):
        """
        menu item should be in json format
        """
        with self.client:
            self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "12389894", "admin")
            response = self.login_user("kasule", "12389894")
            res = json.loads(response.data.decode())
            self.assertTrue(res['auth_token'])
            token = res['auth_token']
            order = self.menu_post("katogo", "any kind", 9000, token)
            self.assertTrue(order.content_type == "application/json")
            self.assertFalse(order.content_type == "text/plain")

    def test_desc_and_meal_not_string(self):
        """
        description and meal should be of string data type
        """
        self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "12389894", "admin")
        response = self.login_user("kasule", "12389894")
        res = json.loads(response.data.decode())
        self.assertTrue(res['auth_token'])
        token = res['auth_token']
        ord = {
            "meal": 2334,
            "description": True,
            "price": 7900,
            "image": "image.jpg"
        }
        rs = self.client.post(
            '/api/v1/menu',
            content_type="application/json",
            headers=dict(Authorization='Bearer' " " + token),
            data=json.dumps(ord)
            )
        self.assertEqual(rs.status_code, 401)
        data = json.loads(rs.data.decode())
        self.assertTrue(data['status'] == 'Failed')
        self.assertTrue(data['message'] == 'Description and Dish must be string format')

    def test_meal_and_desc_not_spaces(self):
        """
        checks whether meal and desc have only spaces
        """
        with self.client:
            self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "12389894", "admin")
            response = self.login_user("kasule", "12389894")
            res = json.loads(response.data.decode())
            self.assertTrue(res['auth_token'])
            token = res['auth_token']
            order = self.menu_post("  ", "   ", 9000, token)
            self.assertEqual(order.status_code, 401)
            data = json.loads(order.data.decode())
            self.assertTrue(data['status'] == 'Failed')
            self.assertTrue(
                data['message'] == 'order request contains spaces only')

    def test_price_not_integer(self):
        """ tests price is integer data type
        """
        with self.client:
            self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "12389894", "admin")
            response = self.login_user("kasule", "12389894")
            res = json.loads(response.data.decode())
            self.assertTrue(res['auth_token'])
            token = res['auth_token']
            order = self.menu_post("kati", "any", "", token)
            self.assertEqual(order.status_code, 401)
            data = json.loads(order.data.decode())
            self.assertTrue(data['status'] == 'Failed')
            self.assertTrue(data['message'] == 'price must be integer')

    def test_fields_not_filled(self):
        """
        fields should not be left un filled
        """
        with self.client:
            self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "12389894", "admin")
            response = self.login_user("kasule", "12389894")
            res = json.loads(response.data.decode())
            self.assertTrue(res['auth_token'])
            token = res['auth_token']
            order = self.menu_post("kati", "any", 0, token)
            self.assertEqual(order.status_code, 401)
            data = json.loads(order.data.decode())
            self.assertTrue(data['status'] == 'Failed')
            self.assertTrue(data['message'] == 'No field should be left empty')

    def test_menu_submited(self):
        with self.client:
            self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "12389894", "admin")
            response = self.login_user("kasule", "12389894")
            res = json.loads(response.data.decode())
            self.assertTrue(res['auth_token'])
            token = res['auth_token']
            order = self.order("chicken", "roasted", 8990, 'new')
            self.assertTrue(order)
            rs = self.menu_post("chicken", "flied", 5000, token)
            Database().add_to_menu("chicken", "flied", 5000)
            data = json.loads(rs.data.decode())
            self.assertEqual(rs.status_code, 201)
            self.assertIn("successfully added to menu", str(data))

    def test_fetch_all_menu_items(self):
        with self.client:
            self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "12389894", "admin")
            response = self.login_user("kasule", "12389894")
            res = json.loads(response.data.decode())
            self.assertTrue(res['auth_token'])
            token = res['auth_token']
            rs = self.menu_post("chicken", "flied", 5000, token)
            Database().add_to_menu("chicken", "flied", 5000)
            data1 = json.loads(rs.data.decode())
            self.assertEqual(rs.status_code, 201)
            result = self.menu_get(1, "dsa", "dsa", 6777)
            data = json.loads(result.data.decode())
            self.assertEqual(result.status_code, 200)
            self.assertIn("Onmenu", str(data))

    def test_delete_menu_item_from_the_menu_list(self):
        """
        admin successfully remove an item from menu list
        """
        with self.client:
            self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "12389894", "admin")
            response = self.login_user("kasule", "12389894")
            res = json.loads(response.data.decode())
            self.assertTrue(res['auth_token'])
            token = res['auth_token']
            order = self.order("chicken", "roasted", 8990, 'new')
            self.assertTrue(order)
            rs = self.menu_post("chicken", "flied", 5000, token)
            Database().add_to_menu("chicken", "flied", 5000)
            data = json.loads(rs.data.decode())
            self.assertEqual(rs.status_code, 201)
            self.assertIn("successfully added to menu", str(data))

            rv = self.menu_delete(token, 1)
            data2 = json.loads(rv.data.decode())
            self.assertEqual(
                data2['success'], 'menu item successfully deleted')
            self.assertEqual(rv.status_code, 200)

    def test_trying_to_delete_menu_item_with_invalid_id(self):
        """
        admin can only delete an item that exist on menu
        """
        with self.client:
            self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "12389894", "admin")
            response = self.login_user("kasule", "12389894")
            res = json.loads(response.data.decode())
            self.assertTrue(res['auth_token'])
            token = res['auth_token']
            rv = self.menu_delete(token, 1)
            data2 = json.loads(rv.data.decode())
            self.assertEqual(data2['failed'], "Please provide a valid menu Id")
            self.assertEqual(rv.status_code, 400)

    def test_user_cant_add_menu_item(self):
        """
        loged in user with user role cant add item to menu
        """
        with self.client:
            self.signup_user(
                "kasule", "kasule@gmail.com", "kansanga", "12389894", "user")
            response = self.login_user("kasule", "12389894")
            res = json.loads(response.data.decode())
            self.assertTrue(res['auth_token'])
            token = res['auth_token']
            order = self.order("chicken", "roasted", 8990, 'new')
            self.assertTrue(order)
            rs = self.menu_post("chicken", "flied", 5000, token)
            Database().add_to_menu("chicken", "flied", 5000)
            data = json.loads(rs.data.decode())
            self.assertEqual(rs.status_code, 409)
            self.assertEqual(
                data['Failed'], 'You dont have permission to add food items to menu')





          