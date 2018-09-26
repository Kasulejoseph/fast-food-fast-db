from flask import json

ID = [0,]
class Order:
    """
    class define order entities and return order dictionary
    """
    def __init__(self, id,dish_name,description,price):
        self.id = Order.id_generator()
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

    def id_generator():
        """
        Generate unique id for each order
        """
        ID[0] = ID[0]+1
        return ID[0]

    def status():
        """
        Generate status list for orders
        """
        status = ['pending','accept','decline','complete']
        return status
