from flask import Flask
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.exc import *
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS

# jwt auth
from constant.http_response import *
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity

# flasgger
from flasgger import Swagger, swag_from
from config.swagger import template, swagger_config

# app config general
app = Flask(__name__)
app.config['SECRET-KEY'] = 'pemmobiledapata'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///kasir_api.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)
CORS(app)

# jwt config app
JWTManager(app= app)
app.config['JWT_SECRET_KEY'] = 'pemmobiledapata'

# flasgger config app
Swagger(app, config= swagger_config, template= template)
app.config['SWAGGER'] = {
    'title' : 'Kasir API',
    'uiversion' : 3
}






