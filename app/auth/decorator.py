from functools import wraps
from flask import request, jsonify, current_app, make_response
import jwt
from app.models.model import User
from app.database.connect import Database


def get_token():
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
        token = token.split(" ")[1]
    if not token:
        return make_response(jsonify({      # pragma: no cover
            'status': 'failed',
            'message': 'Token is missing!'
            }), 401)
    return token


def token_required(f):
    """
    Decotator function to ensure that end points are accessed by
    only authorized users provided they have a valid token
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token()
        try:
            data = jwt.decode(token, 'mysecret')
            user_role = data['role']
            database = Database()
            query = database.get_order_by_value(
                'users', 'email', data['email']
            )
            if not query:
                return {"message": "User not loged in"}, 400
            current_user = User(
                query[0], query[1], query[2], query[3], query[4], query[5])
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.', 401  # pragma: no cover
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.', 401
        return f(current_user, *args, **kwargs)
    return decorated


def role_required():
    token = get_token()
    data = jwt.decode(token, 'mysecret')
    user_role = data['role']
    return user_role


def response(id, username, message, token, status_code):
    """
    method to make http response for authorization token
    """
    return {
        "id": id,
        "username": username,
        "message": message,
        "auth_token": token

    }, status_code


def response_message(status, message, status_code):
    """
    method to handle response messages
    """
    return {
        "status": status,
        "message": message
        }, status_code
