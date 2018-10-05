import jwt
import re
import datetime
from app.database.connect import Database
from app.views.orders import main
from app.models.model import User
from app.auth.decorator import response, response_message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Api, Resource
from flask import make_response, Blueprint, request, jsonify
from flasgger import swag_from
auth = Blueprint('auth', __name__)
db = Database()
api = Api(auth)


class RegisterUser(Resource):
    """
    Class to register a user via api
    """
    @swag_from('../doc/signup.yml')
    def post(self):
        """
        User creates an account
        User sign up details are added to the data base
        """
        if request.content_type != 'application/json':
            return response_message(
                'Bad request', 'Content-type must be in json', 202)   
        detail = request.get_json()
        try:
            if not detail:
                return ({"Failed": "Empty request"}, 400)
            username = detail['username']
            email = detail['email']
            location = detail['location']
            password = generate_password_hash(detail['password'])

            if not username:
                return response_message('Missing', 'Username required', 400)
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return response_message(
                    'Error', 'Missing or wrong email format', 202)
            if not len(detail['password']) > 4:
                return response_message(
                    'Failed', 'Ensure password is morethan 4 characters', 202)
            if not isinstance(username, str):
                return response_message(
                    'Type Error', 'username must all be string', 202)
            if not re.match("^[a-zA-Z0-9_.-]+$", username):
                return response_message(
                    'Space Error', 'Username should not have space, better user -',
                    400)
            if db.get_order_by_value('users', 'email', email):
                return response_message(
                    'Failed', 'User already registered', 409)
            db.insert_into_user(username, email, location, password)
            if detail['role']:
                db.update_role(detail['role'], email)
            return response_message(
                'Success', 'User account successfully created, log in', 201)
        except KeyError as e:
            return ({'KeyError': str(e)})


class LoginUser(Resource):
    """
    Class to register a user via api
    """
    @swag_from('../doc/login.yml')
    def post(self):
        """
        User login if he supplies correct credentials
        token is generated and given to a user
        """
        try:
            if request.content_type != 'application/json':
                return response_message(
                    'Bad request', 'Content-type must be in json', 202)
            detail = request.get_json()
            if not detail:
                return ({"Failed": "Empty request"}, 400)
            username = detail['username']
            password = generate_password_hash(detail['password'])
            if not username and password:
                return response_message(
                    'Failed', 'Username and password are required', 400)
            db_user = db.get_order_by_value('users', 'username', username)
            if not db_user:
                return ({"Failed": "incorect username"}, 401)
            new_user = User(
                db_user[0], db_user[1], db_user[2], db_user[3],
                db_user[4], db_user[5])
            if new_user.username == detail['username'] and check_password_hash(
                    new_user.password, detail['password']):
                payload = {
                    'email': new_user.email,
                    'exp': datetime.datetime.utcnow() +
                    datetime.timedelta(days=60),
                    'iat': datetime.datetime.utcnow(),
                    'sub': new_user.user_id,
                    'role': new_user.role
                }
                token = jwt.encode(
                    payload,
                    'mysecret',
                    algorithm='HS256'
                    )
                if token:
                    return response(
                        new_user.user_id, new_user.username,
                        'You have succesfully logged in.',
                        token.decode('UTF-8'), 200)
            return response_message(
                'Failed', 'incorrect password', 401)
        except KeyError as e:
            return ({'KeyError': str(e)})

api.add_resource(RegisterUser, '/api/v1/auth/signup')
api.add_resource(LoginUser, '/api/v1/auth/login')