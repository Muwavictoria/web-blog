from flask import Blueprint, render_template, session, redirect, url_for, request
from app import mysql
from datetime import datetime
from time import time
from PIL import Image
import MySQLdb.cursors ,os, io , re, base64, unicodedata





admin =  Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')



# login user 
@admin.route('/login', methods=['GET', 'POST'])
def admin_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account: 
            session['loggedin'] = True
            session['id'] = account['admin_id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return  redirect(url_for('admin.admin_dashboard'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('admin_login.html')


# log out user 
@admin.route('/logout')
def admin_logout():
    session.pop('loggedin', None)
    session.pop('admin_id', None)
    session.pop('username', None)
    return redirect(url_for('admin.admin_login'))

# register user 
@admin.route('/register', methods=['GET', 'POST'])
def admin_register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO admin VALUES (NULL, % s, % s, % s, NULL)', (username,password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return redirect(url_for('admin.admin_login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('admin_register.html')




@admin.route('/dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')



@admin.route('/users')
def users():
    return render_template('users.html')


# getting posts 
@admin.route('/posts', methods=['POST','GET'])
def posts():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM post')
        posts = cursor.fetchall()  # Fetch all rows from the result set
        cursor.close()
        return render_template('posts.html', posts=posts)
    return render_template('posts.html')



def slugify(title):
    #  remove assets from characters
    title = unicodedata.normalize('NFKD', title).encode('ASCII', 'ignore').decode('utf-8')

    # Replace non-alpha nummeric characters with hyphens
    title = re.sub(r'[^\w\s-]', '', title).strip().lower() 

    # Replace spaces with hyphens
    title = re.sub(r'[-\s]+', '-', title)

    return title

# adding posts 
@admin.route('/addposts', methods=['GET','POST'])
def addposts():
    if request.method == 'POST' and 'image' in request.files and 'title' in request.form and 'body':
        title = request.form['title']
        body = request.form['body']
        image_file = request.files['image']
        slug = slugify(title)
        created = datetime.now()


        if image_file:
            # Load the image using PIL
            image = Image.open(image_file)
            image_data = io.BytesIO()
            image.save(image_data, 'png')  #it can change to any image format
            image_data = image_data.getvalue()
        else:
            image_data = None

        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO post VALUES (NULL,% s, % s, % s, % s, % s)', (image_data, title, slug, body, created))
        mysql.connection.commit()
        msg = 'You have successfully added products !'

        return redirect(url_for('admin.posts'))
    
    return render_template('posts.html')


#updating posts
@admin.route("/update/<string:id>", methods=['GET','POST'])
def update_post(id):
    if request.method == 'POST':
        new_title = request.form['new_title']
        new_body = request.form['new_body']
        image_file = request.files['new_image']
        new_slug = slugify(new_title)
        new_created = datetime.now()

        if image_file:
            # Load the image using PIL
            image = Image.open(image_file)
            image_data = io.BytesIO()
            image.save(image_data, 'png')  #it can change to any image format
            image_data = image_data.getvalue()
        else:
            image_data = None


        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE post SET image=%s,title=%s, slug = %s, body=%s, created=%s WHERE id = %s',(id,image_data, new_title, new_slug, new_body, new_created))

        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('admin.posts'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM post WHERE id = %s", (id,))
    car = cursor.fetchone()
    cursor.close()

    return render_template('posts.html')

        






#deleting posts posts
@admin.route("/delete/<string:id>", methods=['GET','POST', 'DELETE'])
def delete_post(id):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM `post` WHERE id=%s', (id,))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('admin.posts'))