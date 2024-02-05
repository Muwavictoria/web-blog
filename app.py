from app import app
from app.users.routes import user
from app.posts.routes import post
from app.blog.routes import blog
from app.admin.routes import admin
from app.website.routes import web
# filters.py

import base64

def base64_encode(data):
    return base64.b64encode(data).decode('utf-8')



# Registering Blueprints
app.register_blueprint(user)
app.register_blueprint(post)
app.register_blueprint(blog)
app.register_blueprint(admin)
app.register_blueprint(web)

app.jinja_env.filters['b64encode'] = base64_encode

if __name__ == '__main__':
    app.run(debug=True)