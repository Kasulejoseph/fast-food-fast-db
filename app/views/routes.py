from flask import Flask, request,jsonify,Blueprint,make_response
from flask_restful import Api, Resource, abort
from app.database.connect import Database
from app.auth.decorator import token_required
from app.auth.decorator import response, response_message
from app.models.model import Order

main = Blueprint('main', __name__)
Database = Database()
food_api = Api(main)

class OrderAll(Resource):

    """
    Class has all request methods that 
    uses the end point /api/v1/orders/
    :Admin
    """
    # @token_required
    def get(self):
        all = Database.get_all_orders()
        if all:
            return make_response(jsonify({
                'order_id':all[0][0], 'menu_id':all[0][1], 'user_id':all[0][2], 'meal':all[0][3],
                'desc':all[0][4], 'price':all[0][5], 'status':all[0][6]}),200
                )
        return make_response(jsonify({'error':'no orders posted yet'}),404)

class OrderPost(Resource):
    """
    Class for posting an order request by the user
    :User
    """
    def post(self,current_id=1,menu_id=1):
        data = request.get_json()
        order = Order(data['meal'],data['description'],data['price'],status='new')

        meal = order.dish
        description = order.description
        price = order.price
        status = order.status[0]
        menu_id = menu_id
        current_user = current_id
        if not meal:
            return response_message('Error','meal field cant be left empty', 400)
        if Database.get_order_by_value('orders','meal',meal):
            return response_message('Failed','Order Already Exists', 409)
        Database.insert_into_orders(current_user,menu_id,meal,description,price,status)
        return response_message('Success','Order successfully submited', 201)
        

class OrderById(Resource):
    """
    Admin fetch a specific order from the order list
    :Admin
    """
    def get(self,order_id):
        order_one = Database.get_order_by_value('orders', 'order_id', order_id)
        if order_one:
            response = {'order_id':order_one[0],'meal':order_one[3], 'desc':order_one[4], 'price':order_one[5]}
            user = Database.get_order_by_value('users', 'user_id', order_id)
            return make_response(jsonify({'order':response, 'Order BY':user}),200)

        return response_message('Failed','No order by that Id', 404)
class UpdateStatus(Resource):
    """
    Admin change the status of the order
    status: New->processing->cancelled->complete
    :Admin
    """
    def put(self, order_id):
        data = request.get_json()
        to_update = Database.update_order_status(data['status'],order_id)
        if to_update:
            return response_message('message',to_update, 200)

food_api.add_resource(OrderAll, '/api/v1/orders/')
food_api.add_resource(OrderPost, '/api/v1/users/orders/')
food_api.add_resource(OrderById, '/api/v1/orders/<int:order_id>')
food_api.add_resource(UpdateStatus, '/api/v1/orders/<int:order_id>')