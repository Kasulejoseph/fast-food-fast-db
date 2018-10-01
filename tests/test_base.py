from app import app, app_config
from flask import current_app
from app.database.connect import Database as db
import unittest
import json


class BaseTestCase(unittest.TestCase):

    def create_app(self):
        """
        Create an instance of a class with testing
        """
        app.config.from_object(app_config["testing"])
        return app

    def setUp(self):
        self.client = app.test_client(self)
        with app.app_context():
            connect = db()
            connect.drop_tables()
            connect.create_tables()

    def signup_user(self,username,email,location,password):
        """
        Method to define user registration details
        """
        register = {
            "username": username,
            "email": email,
            "location": location,
            "password": password
        }
        return self.client.post(
            '/api/v1/auth/signup',
            content_type= "application/json",
            data = json.dumps(register)
            )
    def login_user(self,username,password):
        """
        Method to define user login details
        """
        login = {
            "username": username,
            "password": password
        }
        return self.client.post(
            '/api/v1/auth/login',
            content_type = "application/json",
            data = json.dumps(login)
        )

    # def order_post(self,meal,desc,price):
    #     """
    #     Define post attributes and post route
    #     """
    #     data = {
    #         "meal": meal,
    #         "desc": desc,
    #         "price": price
    #     }
    #     return self.client.post(
    #         '/api/v1/orders/',
    #         content_type= "application/json",
    #         data = json.dumps(data)
    #         )
 
    def order_post(self,meal,desc,price):
        """
        Define post attributes and post route
        """
        data = {
            "meal": meal,
            "description": desc,
            "price": price
        }
        return self.client.post(
            '/api/v1/users/orders/',
            content_type= "application/json",
            data = json.dumps(data)
            )



    def tearDown(self):
        with app.app_context():
            connect = db()
            connect.drop_tables()
            connect.create_tables()
    


