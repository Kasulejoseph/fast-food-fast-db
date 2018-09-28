from flask import json

class User:
    """ user class """
    def __init__(self,user_id,username,email,location,password):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password

class Order:
    """
    class define order entities and return order dictionary
    """
    def __init__(self, id,dish_name,description,price):
        self.id = id
        self.dish = dish_name
        self.description = description
        self.price = price
        self.status = Order.status()

    def order_json(self):
        """
        return order in dictionary format
        """
        return  {
            'id': self.id,
            'dish': self.dish,
            'description': self.description,
            'price': self.price,
            'status': self.status[0]

        }

    def status():
        """
        Generate status list for orders
        """
        status = ['pending','accept','decline','complete']
        return status
