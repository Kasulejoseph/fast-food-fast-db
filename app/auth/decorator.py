from functools import wraps
from flask import request, jsonify, current_app,make_response
import jwt
from app.models.model import User
from app.database.connect import Database

def token_required(f):
    """
    Decotator function to ensure that end points are provided by
    only authorized users provided they have a valid token
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return make_response(jsonify({
                'status':'failed',
                'message':'Token is missing!'
                }),401)

        try:
            data = jwt.decode(token,'mysecret')
            database = Database()
            query = database.get_order_by_value(
                'users','email', data['email']
            )
            current_user = User(query[0], query[1], query[2], query[3],query[4])

        except:
            return make_response(jsonify({
                "status": "failed",
                "mesage": "Invalid token"
                }), 401)

        return f(current_user, *args, **kwargs)
    return decorated

def response(self,id, username,message, token):
    """
    method to make http response for authorization token
    """
    return make_response(jsonify({
        "id": id,
        "username": username,
       "message": message,
       "auth_token": token

    })), status_code
