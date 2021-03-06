from flask import Flask, request, jsonify, Blueprint, make_response, json
from flask_restful import Api, Resource, abort
from flasgger import swag_from
from werkzeug import secure_filename
from datetime import datetime
from app.database.connect import Database
from app.auth.decorator import token_required, role_required
from app.auth.decorator import response, response_message
from app.models.model import Order
main = Blueprint('main', __name__)
Database = Database()
food_api = Api(main)


class OrderAll(Resource):
    """
    Class has all request methods that
    uses the end point /api/v1/orders/   :Admin
    """
    @swag_from('../doc/get_all_orders.yml')
    @token_required
    def get(self, current_user):
        if role_required() == 'admin':
            all = Database.get_all_orders()
            all_order_list = []
            if not all:
                return {'error': 'no orders posted yet'}, 404
            for row in all:
                order_dict = {
                    "order_id": row[0],
                    "menu_id": row[1],
                    'user_id': row[2],
                    "meal": row[3],
                    "desc": row[4],
                    "price": row[5],
                    "status": row[6],
                    "date_created": str(row[7])
                }
                all_order_list.append(order_dict)
            return {'Orders': all_order_list}, 200
        return {
            'Failed': 'You dont have permission to access this route'
            }, 409


class OrderPost(Resource):
    """
    Class for posting an order request by the user
    :User
    """
    @swag_from('../doc/create_order.yml')
    @token_required
    def post(current_user, menu_id):
        try:
            data = request.get_json()
            if request.content_type != 'application/json':
                return response_message(
                    'Failed', 'Content type must be application/json', 401)
            id_menu = data['meal_id']
            if not isinstance(id_menu, int):
                return response_message(
                    'Failed', 'menu ids should be of integer data types only', 401)
            if id_menu == 0:
                return response_message(
                    'Failed', 'Zero is not a menu id', 401)
            current_user = current_user.user_id
            order_row = Database.get_order_by_value('menu', 'menu_id', id_menu)
            if not order_row:
                return ({"Message": "No item for that id"}, 404)
            dish = order_row[1]
            desc = order_row[2]
            price = order_row[3]
            Database.insert_into_orders(
                current_user, id_menu, dish, desc, price, status='new')
            return response_message(
                'Success', 'Order successfully submited', 200)
        except KeyError as e:  # pragma: no cover
            return ({'KeyError': str(e)})  # pragma: no cover


class OrderById(Resource):
    """
    Admin fetch a specific order from the order list
    :Admin
    """
    @swag_from('../doc/create_order.yml')
    @token_required
    def get(self, current_user, order_id):
        if role_required() != 'admin':
            return {
                'Failed': 'You dont have permission to access this route'
                }, 409

        order_one = Database.get_order_by_value('orders', 'order_id', order_id)
        if order_one:
            response = {
                'order_id': order_one[0],
                'user_id': order_one[1],
                'meal': order_one[3],
                'desc': order_one[4],
                'price': order_one[5],
                'date': str(order_one[6])
                }
            user = Database.get_order_by_value('users', 'user_id', order_id)
            return ({
                'order': response, 'BY': role_required()
                }), 200
        return response_message('Failed', 'No order by that Id', 404)


class UpdateStatus(Resource):
    """
    Admin change the status of the order
    status: New->processing->cancelled->complete
    :Admin
    """
    @swag_from('../doc/update_order.yml')
    @token_required
    def put(self, current_user, order_id):
        if role_required() != 'admin':
            return ({
                'Failed': 'You dont have permission to access this route'
                }), 409
        if request.content_type != 'application/json':
            return response_message(
                'Failed', 'Content type must be application/json',
                401)
        status = request.get_json()
        if not status:
            return ({"message": "empty request"}), 404
        
        if not isinstance(status['status'], str):
            return response_message(
                'Type Error', 'Status must only be string',
                400) 
        if status['status'].isspace() or len(status['status']) == 0:
            return response_message(
                'Failed', 'Status should not be empty or have only spaces',
                401)
        to_update = Database.update_order_status(status['status'], order_id)
        if to_update:
            return response_message('message', to_update, 200)


class UserHistory(Resource):
    """
    user can view all the order histories
    """
    @swag_from('../doc/get_history.yml')
    @token_required
    def get(current_user, user):
        user_id = current_user.user_id
        order_all = Database.get_order_history_for_a_user(user_id)
        orders = []
        if not order_all:
            return {'error': 'You have not ordered from the site yet'}, 404
        for order in order_all:
            try:
                order_dic = {
                    "order_id": order[0],
                    "menu_id": order[1],
                    'user_id': order[2],
                    "meal": order[3],
                    "desc": order[4],
                    "price": order[5],
                    "status": order[6],
                    "date_created": str(order[7])
                }
                orders.append(order_dic)
            except IndexError as e:
                return {'error': 'You have not ordered from the site yet'}, 404
        return {'Requested': orders}, 200


class MenuAll(Resource):
    """
    User or Admin get all food items on menu
    end point /api/v1/menu/
    :User, Admin
    """
    @swag_from('../doc/get_menu.yml')
    def get(self):
        all = Database.fetch_menu()
        menu_list = []
        if not all:
            return {'error': 'nothing on menu today'}, 404
        for row in all:
            menu_dict = {
                "menu_id": row[0],
                "meal": row[1],
                "desc": row[2],
                "price": row[3],
                "image": row[4]
            }
            menu_list.append(menu_dict)
        return {'Onmenu': menu_list}, 200


class MenuPost(Resource):
    """
    Admin add items to menu
    """
    @token_required
    @swag_from('../doc/add_menu.yml')
    def post(self, current_user):
        if role_required() != 'admin':
            return ({
                'Failed': 'You dont have permission to add food items to menu'
                }), 409
        try:
            data = request.get_json()
            # image = data['image']
            meal = data['meal']
            desc = data['description']
            image = data['image']
            price = data['price']
            if not isinstance(
                    desc, str) or not isinstance(meal, str):
                return response_message(
                    'Failed', 'Description and Dish must be string format', 401)
            if meal.isspace() or desc.isspace():
                return response_message(
                    'Failed', 'order request contains spaces only', 401)
            if not isinstance(price, int):
                return response_message('Failed', 'price must be integer', 401)
            if len(meal) == 0 or len(desc) == 0 or price == 0:
                return response_message(
                    'Failed', 'No field should be left empty', 401)
            order = Order(meal, desc, price, status='new')
            meal = order.dish
            # file = os.path.join("UPLOAD_FOLDER", file)
            # image.append(secure_filename(image.filename)) 
            # print(image)
            if Database.add_to_menu(meal, desc, price, image):
                return {'Failed': 'Error adding a menu'}, 401
            return ({'message': 'successfully added to menu'}, 201)
        except KeyError as e:
            return ({'KeyError': str(e)})


class DeleteMenu(Resource):
    """
    admin deletes item from the menu
    """
    @token_required
    def delete(self, current_user, id):
        if role_required() != 'admin':
            return ({
                'Failed': 'You dont have permission to delete items from menu'
                }), 409
        one = Database.get_order_by_value('menu', 'menu_id', id)
        if one:
            Database.delete_table_column('menu', 'menu_id', id)
            return ({"success": "menu item successfully deleted"}, 200)
        return ({"failed": "Please provide a valid menu Id"}, 400)
        

food_api.add_resource(MenuAll, '/api/v1/menu')
food_api.add_resource(MenuPost, '/api/v1/menu')
food_api.add_resource(DeleteMenu, '/api/v1/menu/<int:id>')
food_api.add_resource(OrderAll, '/api/v1/orders/')
food_api.add_resource(OrderPost, '/api/v1/users/orders/')
food_api.add_resource(OrderById, '/api/v1/orders/<int:order_id>')
food_api.add_resource(UpdateStatus, '/api/v1/orders/<int:order_id>')
food_api.add_resource(UserHistory, '/api/v1/users/orders/')