from get_routes import get_routes_blueprint
from post_routes import post_routes_blueprint
from login_routes import login_routes_blueprint
from flask_cors import CORS, cross_origin


from flask import Flask
app = Flask(__name__)
app.register_blueprint(get_routes_blueprint,url_prefix="/get")
app.register_blueprint(post_routes_blueprint,url_prefix="/add")
app.register_blueprint(login_routes_blueprint,url_prefix="/account")
cors = CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)