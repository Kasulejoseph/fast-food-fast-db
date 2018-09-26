from flask import Flask, request,jsonify,Blueprint,make_response
from flask_restful import Api, Resource, abort
from app.api.models.orders import OrderList

main = Blueprint('main', __name__)
ORDERS = OrderList()
food_api = Api(main)

class OrderAll(Resource):
    """
    Class has all request methods that 
    uses the end point /api/v1/orders/
    """
    def get(self):
        all = ORDERS.get_all_order()
        if all:
            return make_response(jsonify({'Orders': all}),200)
        return make_response(jsonify({'error':'no orders posted yet'}),404)
        
    def post(self):
        if not request.content_type == 'application/json':
            return make_response(jsonify({"failed": 'Content-type must be application/json'}), 401)
        
        data = request.get_json()
        detail = data.get('details')

        if not data:
            return make_response(jsonify({'failed': 'Details keyword and attributes not specified in the request'}), 401)
        if not detail:
            return make_response(jsonify({'failed': 'Details keyword has no attributes specified in the request'}), 400)
        if ORDERS.is_valid_order(detail):
            return make_response(jsonify({'error': ORDERS.is_valid_order(detail)}), 404)
        add = ORDERS.add_order(detail,id)
        return make_response(jsonify({'order': add }),201)


class OrderOne(Resource):
    """
    class combines all request methods that 
    accept order requests by their ids
    """
    def get(self,id):
        #Call get_one_order in ORDERS class to verify the requested id
        one1 = ORDERS.get_one_order(id)

        order_exist = ORDERS.is_order_exist(id)
        if not order_exist:
            return make_response(jsonify({'error': order_exist}),404)        
        if not one1:
            return make_response(jsonify({"invalid":"order id requested not found"}),400)
        return make_response(jsonify({'message': one1}), 200)
        
    #Update status 
    def put(self,id):
        if not request.content_type == 'application/json':
            return make_response(jsonify({"failed": 'Content-type must be application/json'}), 401)
        #Get request in json format
        data = request.get_json()
        detail = data.get('details')
        one1 = ORDERS.get_one_order(id)

        if not data:
            return make_response(jsonify({'failed': 'No attributes specified in the request'}), 401)        
        if not one1:
            return make_response(jsonify({"invalid":"No content found for requested it"}),400)
        if len(detail) !=5:
            abort(404)
    
        #Call update_orders in ORDERS which updates the order status
        update = ORDERS.update_order(detail,id)
        if update:
            return make_response(jsonify({'message': update}),200)

    #Delete order item
    def delete(self,id):
        #Call is_order_exist to confirm whether the passed id is a valid
        order_exist = ORDERS.is_order_exist(id)
        if not order_exist:
            return make_response(jsonify({'error': order_exist}),404)

        #Call ORDERS.delete_one_order(id) to delete the order by id
        delete_one = ORDERS.delete_one_order(id)
        if not delete_one:
            return make_response(jsonify({"failed": "order id to delete not found"}),401)
        return make_response(jsonify({'message': delete_one}), 200)

food_api.add_resource(OrderOne, '/api/v1/orders/<int:id>')
food_api.add_resource(OrderAll, '/api/v1/orders/')