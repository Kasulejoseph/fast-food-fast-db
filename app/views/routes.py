from flask import Flask, request,jsonify,Blueprint,make_response
from flask_restful import Api, Resource, abort
from app.database.connect import Database
from app.auth.decorator import token_required

main = Blueprint('main', __name__)
Database = Database()
food_api = Api(main)

class OrderAll(Resource):

    """
    Class has all request methods that 
    uses the end point /api/v1/orders/
    :Admin
    """
    @token_required
    def get(self):
        all = Database.get_all_orders()
        if all:
            return make_response(jsonify({'Orders': all}),200)
        return make_response(jsonify({'error':'no orders posted yet'}),404)

class OrderPost(Resource):
    """
    Class for posting an order request by the user
    :User
    """
    def post(self):
        pass

class OrderById(Resource):
    """
    Admin fetch a specific order from the order list
    :Admin
    """
    def get(self):
        pass

class UpdateStatus(Resource):
    """
    Admin change the status of the order
    status: New->processing->cancelled->complete
    :Admin
    """
    def put(self):
        pass

food_api.add_resource(OrderAll, '/api/v1/orders/')
food_api.add_resource(OrderPost, '/api/v1/users/orders/')
food_api.add_resource(OrderById, '/api/v1/orders/<int:order_id>')
food_api.add_resource(UpdateStatus, '/api/v1/orders/<int:order_id>')