from flask import Flask
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.exc import *
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS

# tambahan baru
from constant.http_response import *
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity


app = Flask(__name__)
app.config['SECRET-KEY'] = 'pemmobiledapata'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///kasir_api.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)
CORS(app)
# tambahan baru
JWTManager(app= app)
app.config['JWT_SECRET_KEY'] = 'pemmobiledapata'


