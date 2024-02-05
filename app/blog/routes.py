from flask import Blueprint, render_template, request, redirect, url_for

from app.models import Post
from app import mysql
import re, MySQLdb

blog = Blueprint('blog', __name__, url_prefix='/blog',template_folder='templates')


@blog.route("/", methods=["GET", "POST"])
def blog_posts():
    return render_template("index.html")

@blog.route('/home', methods=['GET','POST'])
def home():
    if request.method == "GET":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM post')
        posts = cursor.fetchall()  # Fetch all rows from the result set
        cursor.close() 
        return render_template('blog.html', posts=posts )       
    return render_template('blog.html')

@blog.route('/cars')
def products():
    return render_template('products.html')

@blog.route('/readmore/<string:id>', methods=['GET', 'POST'])
def readmore(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM post WHERE id = %s', (id))
    post = cursor.fetchone()
    cursor.execute('SELECT * FROM post')
    posts = cursor.fetchall()  # Fetch all rows from the result set
    cursor.close() 
    return render_template('readmore.html', post=post, posts=posts)
        

