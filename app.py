from app import app
from app.blog.routes import blog
from app.admin.routes import admin
# filters.py

import base64

def base64_encode(data):
    return base64.b64encode(data).decode('utf-8')



# Registering Blueprints
app.register_blueprint(blog)
app.register_blueprint(admin)

app.jinja_env.filters['b64encode'] = base64_encode

if __name__ == '__main__':
    app.run(debug=True)