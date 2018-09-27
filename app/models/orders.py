from flask import json
from app.models.dish import Order

class OrderList:
    """
    data structures
    """
    def __init__(self):
        self.order_list = []

    def is_order_exist(self, id):
        """check if order not exist in the order list """
        for order in self.order_list:
            if order['id'] != id:
                return "bad request, order not found"

    def is_valid_order(self, order_data):
        """ check whether order is a valid one """
        details = order_data
        dish = details['dish']
        desc = details['description']
        price = details['price']
        if not isinstance(desc, str):
            return "Description should be string format"
        if not isinstance(dish, str):
            return "Dish should be in string format"
        if not isinstance(price, int):
            return "price should be integer"
        if dish.isspace() or desc.isspace() :
            return "order request contains spaces only"
        if len(dish)==0 or len(desc) == 0 or price == 0:
            return "No field should be left empty"
        self.order = Order(id,dish.lower(),desc.lower(),price)
        if not self.order:
            return "invalid order"

    def add_order(self,order_data,id):
        """
        create an order in not exists
        """
        order_dict = self.order.order_json()
        if order_dict in self.order_list:
            return "Order already exist"
        self.order_list.append(order_dict)
        return "order added successfully"

    def get_all_order(self):
        """
        get all orders posted
        """
        if self.order_list is not None:
            return self.order_list
        return "order list empty"

    def get_one_order(self,id):
        """
        get one order by its id
        """
        for order in self.order_list:
            if order['id'] == id:
                return order

    def update_order(self,details,id):
        """ update the status of the order 
        """
        order = self.get_one_order(id)
        status = details['status'].lower()
        sta = Order.status()            #get status list from order class                                                                        
        if status not in sta:
            return "invalid order status"
        if order['id'] == id:
            sta[0] = details['status']
            order['status'] = sta[0]
            return "status updated successfully"


    def delete_one_order(self, id):
        """ delete an order by its id
        """
        order = self.get_one_order(id)
        if order :
            self.order_list.remove(order)
            return "deleted successfully"

        
        

    
