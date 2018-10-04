from flask import json


class User:
    """ user class """
    def __init__(self, user_id, username, email, location, password, role):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.role = role


class Order:
    """
    class define order entities and return order dictionary
    """
    def __init__(self, dish_name, description, price, status):
        self.dish = dish_name
        self.description = description
        self.price = price
        self.status = Order.status()

    def order_json(self):
        """
        return order in dictionary format
        """
        return {
            'dish': self.dish,
            'description': self.description,
            'price': self.price,
            'status': self.status[0]

        }

    def status():
        """
        Generate status list for orders
        """
        status = ['New', 'processing', 'cancelled', 'complete']
        return status
