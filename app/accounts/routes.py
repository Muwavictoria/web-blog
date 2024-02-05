from flask import Blueprint,render_template


auth = Blueprint('auth', __name__, url_prefix='/auth', static_folder='static', template_folder='templates')



@auth.route('/login')
def login():
    return render_template('login.html')
@auth.route('/register')
def register():
    return render_template('register.html')
@auth.route('/logout')
def logout():
    return render_template('Login.html')