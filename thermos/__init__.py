import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Configure database
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = b"2\xcf\xcc\xd1M'\xe9_a9u\x1c\xf65\xfa\x10/Ac\xf0\xc6\xc4q\x99"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.init_app(app)

import thermos.models
import thermos.views