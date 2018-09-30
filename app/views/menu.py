from flask import Flask, request,jsonify,Blueprint,make_response
from flask_restful import Api, Resource, abort
from app.database.connect import Database

main = Blueprint('main', __name__)
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
        pass

food_api.add_resource(MenuAll, '/api/v1/menu')
food_api.add_resource(MenuPost, '/api/v1/menu')