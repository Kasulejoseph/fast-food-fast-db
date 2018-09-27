from app import app, app_config
from flask import current_app
from app.models.dish import Order
import unittest


class BaseTestCase(unittest.TestCase):

    def create_app(self):
        """
        Create an instance of a class with testing
        """
        app.config.from_object(app_config["testing"])
        return app

    def setUp(self):
        self.client = app.test_client(self)
        self.order = {'details': {
            'id':3 ,
            'dish': "jgh",
            'description': "description",
            'price': 34
        }}
    
    def test_app_exists(self):
        self.assertFalse(self.create_app is None)

    def test_order_class(self):
        """ Test order parameters """
        self.assertTrue(Order(1,"KATOGO",'all',2330))

    def test_order_json(self):
        """ Test order return dict format """
        self.order = Order(1,"KATOGO",'all',2330)
        dict_type = type(self.order.order_json())
        self.assertEqual(dict_type,dict)

    def test_id_is_integer(self):
        int_id = type(Order.id_generator())
        self.assertEqual(int_id,int)

    def test_status_not_empty(self):
        status_len = len(Order.status())
        self.assertTrue(status_len!=0)

    def test_status_is_valid(self):
        self.order = Order(1,"KATOGO",'all',2330)
        status = ['pending','accept','decline','complete']
        self.assertEqual(Order.status(),status)

    def test_status_is_not_valid(self):
        self.order = Order(1,"KATOGO",'all',2330)
        status = ['pending','accept','decline']
        self.assertNotEqual(Order.status(),status)

