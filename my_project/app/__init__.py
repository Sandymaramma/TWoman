from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '0c4bdc6795503f3d38a8cc9992879d9a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tWoman.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from app import routes