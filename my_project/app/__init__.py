from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '0c4bdc6795503f3d38a8cc9992879d9a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tWoman.db'

db = SQLAlchemy(app)

from app import routes