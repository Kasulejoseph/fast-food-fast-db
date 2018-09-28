import jwt
from app.database.connect import Database
from app.views.routes import main
from app.models.model import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Api,Resource
from datetime import datetime, timedelta
from flask import make_response,Blueprint,request,jsonify
main = Blueprint('main', __name__)
db = Database()
api = Api(main)

class RegisterUser(Resource):
    def post(self):
        detail = request.get_json()
        username = detail['username']
        email = detail['email']
        location = detail['location']
        password = generate_password_hash(detail['password'])
        if not username:
            make_response(jsonify({'message': "username required"}), 400)
        if not email:
            make_response(jsonify({'message': "email required"}), 400)
        if not location:
            make_response(jsonify({'message': "location required"}), 400)
        if not password:
            make_response(jsonify({'message': "password required please"}), 400)
        if db.get_order_by_value('users','email',email):
            return make_response(jsonify({"message":"User already registered"}), 409)
        db.insert_into_user(username, email,location,password)
        return make_response(jsonify({'message':"User account successfully registered"}),201)

class LoginUser(Resource):
    def post(self):
        detail = request.get_json()
        username = detail['username']
        password = generate_password_hash(detail['password'])
        if not username:
            make_response(jsonify({'message': "username required"}), 400)
        if not password:
            make_response(jsonify({'message': "password required"}), 400)
        if len(password)<6:
            make_response(jsonify({'message': "password too short, should be more that 6 characters"}), 400)
        db_user = db.get_order_by_value('users','username',username)
        new_user = User(db_user[0],db_user[1],db_user[2],db_user[3],db_user[4])
        if new_user.username == detail['username'] and check_password_hash(new_user.password, detail['password']):
            #token
            token = jwt.encode(
                {'email':new_user.email,
                'exp':datetime.utcnow() + timedelta(days=10, minutes=50)
                }, 'mysecret'
                )
            
            if token:
                response = {
                    'message': 'You have succesfully logged in.',
                    'token':token.decode('UTF-8'),
                    'username': new_user.username,
                    'email': new_user.email,
                    'Id': new_user.user_id
                }  
            return make_response(jsonify(response), 200)
        return make_response(jsonify({"mesage":"Check your username or password"}), 401)
        

api.add_resource(RegisterUser,'/api/v1/auth/signup')
api.add_resource(LoginUser,'/api/v1/auth/login')