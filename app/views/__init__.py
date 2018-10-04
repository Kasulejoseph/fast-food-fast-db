from flask import Blueprint, jsonify
from flask_restful import Api

main = Blueprint('main', __name__)
food_api = Api(main)
