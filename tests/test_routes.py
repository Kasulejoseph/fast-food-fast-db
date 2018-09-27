from tests.test_base import BaseTestCase
from app.models.orders import OrderList

import unittest
import json

class TestOrderRoutes(BaseTestCase):
    """ 
    Test case to test end points
    :routes.py
    :order.py
    """

    def test_order_creation(self):
        """ Test status code whenever order is successfully created """
        result = self.client.post(
            '/api/v1/orders/',
            content_type = 'application/json',
            data=json.dumps(self.order)
        )
        self.assertEqual(result.status_code,201)

    def test_no_details_keyword_in_order_request(self):
        """ Test detail keyword is not passed with the order post """
        self.order = {}
        result = self.client.post(
            '/api/v1/orders/',
            content_type = 'application/json',
            data=json.dumps(self.order)
        )
        self.assertEqual(result.status_code,401)
        self.assertIn('Details keyword and attributes not specified in the request',str(result.data))
    
    def test_no_content_in_order_request(self):
        """ Test detail keyword is passed but with
            empty content or order item
        """
        self.order = { 'details':{}}
        result = self.client.post(
            '/api/v1/orders/',
            content_type = 'application/json',
            data=json.dumps(self.order)
        )
        self.assertEqual(result.status_code,400)
        self.assertIn('Details keyword has no attributes specified in the request',str(result.data))
    
    def test_order_can_be_added_to_list_and_fetched(self):
        """ 
        Test order can be appended to order lists(POST)
        After updating the order get that item by id(GET) 
        Then try to get that order by id which is invalid (GET)
        """
        self.list = []
        self.order = {'details': {
            'id':3 ,
            'dish': "jgh",
            'description': "description",
            'price': 34
        }}
        #update order (POST)
        result = self.client.post(
            '/api/v1/orders/',
            content_type = 'application/json',
            data=json.dumps(self.order)
        )
        self.list.append(self.order)
        self.assertEqual(result.status_code,201)
        self.assertIn("order added successfully",str(result.data))

        #get order by its id (GET)
        result = self.client.get(
            '/api/v1/orders/25',
            content_type ='aplication/json',
            data = json.dumps(self.order)
        )
        self.assertEqual(result.status_code,200)
        self.assertIn('"id": 25',str(result.data))

        #try to get order by an id which doesnt exist (GET) id = 1000
        result = self.client.get(
            '/api/v1/orders/1000',
            content_type ='aplication/json',
            data = json.dumps(self.order)
        )
        self.assertEqual(result.status_code,400)
        self.assertIn('order id requested not found',str(result.data))

    def test_request_not_json(self):
        """ Test order content to be posted not in json format """
        result = self.client.post(
            '/api/v1/orders/',
            content_type = 'text/css',
            data=json.dumps(self.order)
        )
        self.assertEqual(result.status_code,401)
        self.assertIn('Content-type must be application/json',str(result.data))

    def test_get_order_when_no_orders_in_order_list(self):
        """ Test can't get orders when their is no food items available """
        list = []
        result = self.client.get(
            '/api/v1/orders/',
            content_type = 'application/json',
            data  = json.dumps(list)
        )
        #tests
        self.assertEqual(result.status,'404 NOT FOUND')
        self.assertIn('no orders posted yet',str(result.data))
        
    def test_request_get_all_orders(self):
        """ Test can fetch all orders """
        self.list = [{
            'id':3 ,
            'dish': "jgh",
            'description': "description",
            'price': 34
        }]
        result = self.client.get(
            '/api/v1/orders/',
            content_type = 'application/json',
            data = json.dumps(self.list)
        )
        data = json.loads(result.data.decode())
        self.assertEqual(result.status,'200 OK')
        self.assertTrue(result)
        self.assertIsInstance(data['Orders'], list)
        self.assertTrue(len(data['Orders']) != 0)
        self.assertIn('"price": 34',str(result.data))

    def test_cant_get_order_which_doesnt_exist(self):
        """ 
        Test that you can get an order
        from empty order list 
        """
        self.list = []
        result = self.client.get(
            '/api/v1/orders/23',
            content_type ='aplication/json',
            data = json.dumps(self.list)
        )
        self.assertEqual(result.status_code,404)
        self.assertIn("null",str(result.data))

    def test_update_not_in_json(self):
        """
        Test that status order update 
        request is in application/json format 
        """
        result = self.client.put(
            '/api/v1/orders/1',
            content_type = 'text/css',
            data=json.dumps(self.order)
        )
        self.assertEqual(result.status_code,401)
        self.assertIn('Content-type must be application/json',str(result.data))

    def test_update_has_no_details_keyword_in_order_request(self):
        """ 
        Test whether update request has detail 
        keyword parsed with the order post 
        """
        self.order = {}
        result = self.client.put(
            '/api/v1/orders/1',
            content_type = 'application/json',
            data=json.dumps(self.order)
        )
        self.assertEqual(result.status_code,401)
        self.assertIn('No attributes specified in the request',str(result.data))

    def test_id_has_no_corresponding_data(self):
        """ Test can't update a non existing order item """
        result = self.client.put(
            '/api/v1/orders/2',
            content_type = 'application/json',
            data = json.dumps(self.order)
        )
        self.assertEqual(result.status_code,400)
        self.assertIn("No content found for requested it", str(result.data))
    
    def test_incoming_update_is_valid(self):
        """
        Test that the incoming request is valid with 5 items
        """
        self.list = []
        self.order = {'details': {
            'dish': "jgh",
            'description': "description",
            'price': 34
        }}
        result = self.client.post(
            '/api/v1/orders/',
            content_type = 'application/json',
            data=json.dumps(self.order)
        )
        self.list.append(self.order)
        data = json.loads(result.data.decode())
        self.assertEqual(result.status_code,201)
        #self.assertIn("peasd",str(data))
        self.assertIn("order added successfully",str(result.data))
        
        rs = self.client.put(
            '/api/v1/orders/23',
            content_type = 'application/json',
            data= json.dumps(self.order)
        )
        #data = json.loads(rs.data.decode())
        self.assertIn('order added successfully',str(data['order']))
        self.assertEqual(rs.status_code,404)

    def test_cant_delete_food_item_when_food_list_empty(self):
        """ 
        A request to delete a food item
        from an empty food item list fails
        """
        rs = self.client.delete(
            '/api/v1/orders/4',
            content_type = 'application/json',
            data = json.dumps(self.order)
        )
        self.assertEqual(rs.status_code,404)
        self.assertIn("null",str(rs.data))

    def test_to_delete_order_by_invalid_id(self):
        """
        Trying to delete a food item from order list with 
        invalid id fails
        :id = 1000
        """
        self.list = []
        self.order = {'details': {
            'dish': "jgh",
            'description': "description",
            'price': 34
        }}
        #first post to the list
        result = self.client.post(
            '/api/v1/orders/',
            content_type = 'application/json',
            data=json.dumps(self.order)
        )
        #append to list and test for post         
        self.list.append(self.order)
        self.assertEqual(result.status_code,201)
        self.assertIn("order added successfully",str(result.data))

        #try to delete item with id 1000 that dont exist in the list
        rs = self.client.delete(
            '/api/v1/orders/1000',
            content_type = 'application/json',
            data = json.dumps(self.order)
        )
        #tests
        self.list.remove(self.order)
        self.assertEqual(rs.status_code,401)
        self.assertIn("order id to delete not found",str(rs.data))

    def test_kasule_order_deleted_by_id(self):
        """
        Delete order item by its id
        :id =23
        """
        list = []
        order = {'details': {
            'dish': "jgh",
            'description': "description",
            'price': 34
        }}
        #first post to the list
        rv = self.client.post(
            '/api/v1/orders/',
            content_type = 'application/json',
            data=json.dumps(order)
        )
        #append to list and test for post         
        list.append(order)
        data = json.loads(rv.data.decode())
        self.assertEqual(rv.status_code,201)
        self.assertIn("order added successfully",str(rv.data))

        #delete the food item by its id 23
        rs = self.client.delete(
            '/api/v1/orders/23',
            content_type = 'application/json',
            data = json.dumps(order)
        )
        #tests
        list.remove(order)
        self.assertEqual(rs.status_code,200)
        self.assertIn("deleted",str(rs.data))

    def test_order_can_be_updated(self):
        self.list = []
        self.order = {'details': {
            'dish': "jgh",
            'description': "description",
            'price': 34
        }}
        result = self.client.post(
            '/api/v1/orders/',
            content_type = 'application/json',
            data=json.dumps(self.order)
        )
        self.list.append(self.order)
        data = json.loads(result.data.decode())
        self.assertEqual(result.status_code,201)
        #self.assertIn("peasd",str(data))
        self.assertIn("order added successfully",str(result.data))

        rs = self.client.put(
            '/api/v1/orders/26',
            content_type = 'application/json',
            data= json.dumps({'details':
                {'price': 34, 
                'description': 'description',
                'dish': 'jgh', 
                'status': 'finished',
                'id': 26
            }})
        )
        data = json.loads(rs.data.decode())
        self.assertIn('invalid order status',str(data))
        self.assertEqual(rs.status_code,200)
    
        rs = self.client.put(
            '/api/v1/orders/26',
            content_type = 'application/json',
            data= json.dumps({'details':
                {'price': 34, 
                'description': 'description',
                'dish': 'jgh', 
                'status': 'complete',
                'id': 26
            }})
        )
        data = json.loads(rs.data.decode())
        self.assertIn('status updated successfully',str(data))
        self.assertEqual(rs.status_code,200)
        
    def test_attribute_dish_not_strings(self):
        """ Test Dish not strings """
        self.order = {'details': {
            'dish': 6787,
            'description': "description",
            'price': 34
        }}
        result = self.client.post(
            '/api/v1/orders/',
            content_type = 'application/json',
            data=json.dumps(self.order)
        )
        self.assertEqual(result.status_code,404)
        self.assertIn('Dish should be in string format',str(result.data))
    
    def test_description_not_strings(self):
        """ Test description is not strings """
        self.order = {'details': {
            'dish': "6787",
            'description': 60000,
            'price': 34
        }}
        result = self.client.post(
            '/api/v1/orders/',
            content_type = 'application/json',
            data=json.dumps(self.order)
        )
        self.assertEqual(result.status_code,404)
        self.assertIn('Description should be string format',str(result.data))
        
    def test_price_should_be_integer(self):
        """ Test price is integer """
        self.order = {'details': {
            'dish': "buffer",
            'description': "mawogo",
            'price': "sente"
        }}
        result = self.client.post(
            '/api/v1/orders/',
            content_type = 'application/json',
            data=json.dumps(self.order)
        )
        self.assertEqual(result.status_code,404)
        self.assertIn('price should be integer',str(result.data))

    def test_spaces_as_inputs(self):
        """ Test dish and description have only spaces """
        self.order = {'details': {
            'dish': " ",
            'description': " ",
            'price': 9000
        }}
        result = self.client.post(
            '/api/v1/orders/',
            content_type = 'application/json',
            data=json.dumps(self.order)
        )
        self.assertEqual(result.status_code,404)
        self.assertIn('order request contains spaces',str(result.data))

    def test_dish_and_description_has_empty_string(self):
        """ Test dish and description are not empty strings """
        self.order = {'details': {
            'dish': "",
            'description': "",
            'price': 0
        }}
        result = self.client.post(
            '/api/v1/orders/',
            content_type = 'application/json',
            data=json.dumps(self.order)
        )
        self.assertEqual(result.status_code,404)
        self.assertIn('No field should be left empty',str(result.data))

