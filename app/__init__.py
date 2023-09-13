from .config import DevelopmentConfig
from flask import Flask, jsonify, g
#from db import db, ma 
from .CIE.views import CIE, home
from .login.views import token
from .swagger.views import swagger


import json
from functools import wraps
import sys
from flask_jwt_extended import JWTManager
from .login.models import User

#ACTIVE_ENDPOINTS = [('/',home), ('/dashboard', dashboard), ('/releases', releases), ('/artists', artists), ('/purchase', purchase), ("/products", products) ]
ACTIVE_ENDPOINTS = [('/',home),('/CIE',CIE), ('/token', token) ,('/swagger', swagger) ]

login_manager = None
ldap_manager = None


def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    
    app.config.from_object(config)
    #app.config.from_envvar('CONFIG_SETTINGS')

    #db.init_app(app)
    #ma.init_app(app)


    #with app.app_context():
    #    db.create_all()

    # register each active blueprint
    for url, blueprint in ACTIVE_ENDPOINTS:
        app.register_blueprint(blueprint, url_prefix=url)


    app.config["JWT_SECRET_KEY"] = "holaMundo" 

    #app.config['SERVER_NAME'] = 'localhost:5000'

    app.config['SECRET_KEY'] = 'secret'
    app.config['DEBUG'] = True


    
    return app


def ldap_auth_required():
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not g.ldap_authenticated:
                return jsonify({'message': 'Acceso no autorizado'}), 401
            return func(*args, **kwargs)

        return decorated_function

    return decorator




if __name__ == "__main__":
    app_flask = create_app()
    print(str(app_flask.debug), file=sys.stderr)
    app_flask.run()





