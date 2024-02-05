from flask import Flask
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.secret_key = 'your secret key'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"

app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'blog'


mysql = MySQL(app)
db = SQLAlchemy(app)

from app import models


