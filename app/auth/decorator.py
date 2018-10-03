from functools import wraps
from flask import request, jsonify, current_app,make_response
import jwt
from app.models.model import User
from app.database.connect import Database 
def get_token():
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']

    token = token.split(" ")[1]

    if not token:
        return make_response(jsonify({
            'status':'failed',
            'message':'Token is missing!'
            }),401)
    return token

def role_required(user):
    return user
def token_required(f):
    """
    Decotator function to ensure that end points are provided by
    only authorized users provided they have a valid token
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token()
        try:
            data = jwt.decode(token,'mysecret')
            user_role = data['role']
            # role_required(user = user_role)
            database = Database()
            query = database.get_order_by_value(
                'users','email', data['email']
            )
            current_user = User(query[0], query[1], query[2], query[3],query[4])
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.' 
        except:
            return make_response(jsonify({
                "status": "failed",
                "mesage": "Invalid token"
                }), 401)

        return f(current_user, *args, **kwargs)
    return decorated

def role_required():
    token = get_token()
    data = jwt.decode(token,'mysecret')
    user_role = data['role']
    return user_role

def response(id, username, message, token, status_code):
    """
    method to make http response for authorization token
    """
    return make_response(jsonify({
        "id": id,
        "username": username,
       "message": message,
       "auth_token": token

    }), status_code)

def response_message(status,message,status_code):
    """
    method to handle response messages
    """
    return make_response(jsonify({
        "status": status,
        "message": message
    }), status_code)
    
