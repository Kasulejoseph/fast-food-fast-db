from flask import Flask 
from app.views.orders import main
from app.auth.views import auth
from instance.config import app_config

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(app_config["development"])
app.register_blueprint(main)
app.register_blueprint(auth)

from app.auth import views