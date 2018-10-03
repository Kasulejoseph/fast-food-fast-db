from app.views.orders import OrderAll, OrderPost, OrderById, UpdateStatus
from tests.test_base import BaseTestCase
from app.database.connect import Database
import json
db = Database()

class TestOrder(BaseTestCase):


    # def test_order_in_json(self):
    #     with self.client:
    #         order = self.order_post("katogo","any kind",9000)
    #         self.assertTrue(order.content_type=="application/json")
    #         self.assertFalse(order.content_type=="text/plain")

    def test_desc_and_meal_not_string(self):
        ord = { 
            "meal": 2334,
            "description": True,
            "price": 7900
        }
        rs = self.client.post(
            '/api/v1/users/orders/',
            content_type= "application/json",
            data = json.dumps(ord)
            )
        self.assertEqual(rs.status_code, 401)
        data = json.loads(rs.data.decode())
        self.assertTrue(data['status']== 'Failed')
        self.assertTrue(data['message']== 'Description and Dish must be string format')

    def test_meal_and_desc_not_spaces(self):
        with self.client:
            order  = self.order_post("  ","   ",9000)
            self.assertEqual(order.status_code, 401)
            data = json.loads(order.data.decode())
            self.assertTrue(data['status'] == 'Failed')
            self.assertTrue(data['message'] == 'order request contains spaces only')

    def test_price_not_integer(self):
        with self.client:
            order  = self.order_post("kati","any","")
            self.assertEqual(order.status_code, 401)
            data = json.loads(order.data.decode())
            self.assertTrue(data['status'] == 'Failed')
            self.assertTrue(data['message'] == 'price must be integer')

    def test_fields_not_filled(self):
        with self.client:
            order  = self.order_post("kati","any",0)
            self.assertEqual(order.status_code, 401)
            data = json.loads(order.data.decode())
            self.assertTrue(data['status'] == 'Failed')
            self.assertTrue(data['message'] == 'No field should be left empty')

    # def test_succesful_order_creation(self):
    #     with self.client:
    #         order  = {
    #             "user_id": 1,
    #             "meal": "luwombo",
    #             "description": "any kind",
    #             "price": 9000,
    #             "status": "New"
    #         }
    #         Database().add_to_menu('luwombo','any','4000')
    #         Database().insert_into_user("kasule", "email@gmail.com","location", "password")
    #         # Database.insert_into_orders(1,"menu_id","meal,description",9000,"new")
    #         rs = self.client.post(
    #         '/api/v1/users/orders/',
    #         content_type= "application/json",
    #         data = json.dumps(order)
    #         )
    #         self.assertEqual(rs.status_code, 201)
    #         data = json.loads(rs.data.decode())
    #         self.assertTrue(data['status'] == 'Success')
    #         self.assertTrue(data['message'] == 'Order successfully submited')

            



