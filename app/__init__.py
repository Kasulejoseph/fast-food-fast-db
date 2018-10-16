from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from app.views.orders import main
from app.auth.views import auth
from app.auth import views
from instance.config import app_config

app = Flask(__name__, instance_relative_config=True)
CORS(app)
app.config.from_object(app_config["development"])
Swagger(app)
app.register_blueprint(main)
app.register_blueprint(auth)
