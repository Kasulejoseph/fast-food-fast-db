from flask import Flask, request, jsonify, Blueprint, make_response
from flask_restful import Api, Resource, abort
from app.database.connect import Database
from app import main

Database = Database()
food_api = Api(main)


class MenuAll(Resource):
    """
    User or Admin get all food items on menu
    end point /api/v1/menu/
    :User, Admin
    """
    def get(self):
        all = Database.fetch_menu()
        if all:
            return make_response(jsonify({'Orders': all}),200)
        return make_response(jsonify({'error':'Nothing on menu'}),404)

class MenuPost(Resource):
    """
    Class for posting an order request by the user
    :User
    """
    def post(self):
        data = request.get_json()
        meal = data['meal']
        desc = data['description']
        price = data['price']
        if Database.add_to_menu(meal,desc,price):
            return make_response(jsonify({'message':'successfully added to menu'}), 201)
        return make_response(jsonify({'Failed': 'Error adding a menu'}))

food_api.add_resource(MenuAll, '/api/v1/menu')
food_api.add_resource(MenuPost, '/api/v1/menu')