from tests.test_base import BaseTestCase
from app.models.orders import OrderList
from app.models.dish import Order

import unittest
class OrderTestClass(BaseTestCase):

    def test_order_list_empty(self):
        pass

    def test_is_order_exist(self):
        id2 = 4
        bb = OrderList().is_order_exist
        self.assertTrue(bb)

    def test_is_valid_order(self):
        details =  {
            'id':3 ,
            'dish': "",
            'description': "self.description",
            'price': [54,54,45]

        }
        self.order = Order(id,details['dish'],details['description'],details['price'])
        self.assertTrue(self.order)
        
    def test_order_list_is_none(self):
        self.assertTrue(OrderList().get_all_order)



    
