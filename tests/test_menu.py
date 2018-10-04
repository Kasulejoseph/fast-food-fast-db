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
            order = self.menu_post("katogo", "any kind", 9000)
            self.assertTrue(order.content_type == "application/json")
            self.assertFalse(order.content_type == "text/plain")

    def test_desc_and_meal_not_string(self):
        """
        description and meal should be of string data type
        """
        ord = {
            "meal": 2334,
            "description": True,
            "price": 7900
        }
        rs = self.client.post(
            '/api/v1/menu',
            content_type="application/json",
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
            order = self.menu_post("  ", "   ", 9000)
            self.assertEqual(order.status_code, 401)
            data = json.loads(order.data.decode())
            self.assertTrue(data['status'] == 'Failed')
            self.assertTrue(data['message'] == 'order request contains spaces only')

    def test_price_not_integer(self):
        """ tests price is integer data type
        """
        with self.client:
            order = self.menu_post("kati", "any", "")
            self.assertEqual(order.status_code, 401)
            data = json.loads(order.data.decode())
            self.assertTrue(data['status'] == 'Failed')
            self.assertTrue(data['message'] == 'price must be integer')

    def test_fields_not_filled(self):
        """
        fields should not be left un filled
        """
        with self.client:
            order = self.menu_post("kati", "any", 0)
            self.assertEqual(order.status_code, 401)
            data = json.loads(order.data.decode())
            self.assertTrue(data['status'] == 'Failed')
            self.assertTrue(data['message'] == 'No field should be left empty')

    def test_menu_submited(self):
        with self.client:
            order = self.order("chicken", "roasted", 8990, 'new')
            self.assertTrue(order)
            rs = self.menu_post("chicken", "flied", 5000)
            Database().add_to_menu("chicken", "flied", 5000)
            data = json.loads(rs.data.decode())
            self.assertEqual(rs.status_code, 201)
            self.assertIn("successfully added to menu", str(data))

    def test_fetch_all_menu_items(self):
        with self.client:
            rs = self.menu_post("chicken", "flied", 5000)
            Database().add_to_menu("chicken", "flied", 5000)
            data1 = json.loads(rs.data.decode())
            self.assertEqual(rs.status_code, 201)
            result = self.menu_get(1, "dsa", "dsa", 6777)
            data = json.loads(result.data.decode())
            self.assertEqual(result.status_code, 200)
            self.assertIn("Onmenu", str(data))
            