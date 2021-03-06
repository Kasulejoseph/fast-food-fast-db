from app import app, app_config
from flask import current_app
from instance import config
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

    def tearDown(self):
        with app.app_context():
            connect = db()
            connect.drop_tables()
            connect.create_tables()
    
    def signup_user(self, username, email, location, password, role):
        """
        Method to define user registration details
        """
        register = {
            "username": username,
            "email": email,
            "location": location,
            "password": password,
            "role": role
        }
        return self.client.post(
            '/api/v1/auth/signup',
            content_type="application/json",
            data=json.dumps(register)
            )

    def login_user(self, username, password):
        """
        Method to define user login details
        """
        login = {
            "username": username,
            "password": password
        }
        return self.client.post(
            '/api/v1/auth/login',
            content_type="application/json",
            data=json.dumps(login)
        )

    def menu_post(self, meal, desc, price, token):
        """
        Define post attributes and route
        """
        data = {
            "meal": meal,
            "description": desc,
            "price": price,
            "image": "image.jpg"
        }
        return self.client.post(
            '/api/v1/menu',
            headers=dict(Authorization='Bearer' " " + token),
            content_type="application/json",
            data=json.dumps(data)
            )

    def menu_get(self, id, meal, desc, price):
        """
        set the fetch menu test method
        """
        data = {
            "id": id,
            "meal": meal,
            "description": desc,
            "price": price,
            "image": "image.jpg"
        }
        return self.client.get(
            '/api/v1/menu',
            content_type="application/json",
            data=json.dumps(data)
            )

    def menu_delete(self, token, id):
        """
        test method for deleting an item from menu
        """
        return self.client.delete(
            '/api/v1/menu/1',
            headers=dict(Authorization='Bearer' " " + token),
            content_type="application/json"
        )

    def order(self, meal, desc, price, status):
        return {
            "meal": meal,
            "desc": desc,
            "price": price,
            "status": status
        }

