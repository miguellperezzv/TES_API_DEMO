from .config import DevelopmentConfig
from flask import Flask, session, request, jsonify, g
#from db import db, ma 
from .CIE.views import CIE, home
from .login.views import token
from flask_swagger_ui import get_swaggerui_blueprint
from flask_ldap3_login import LDAP3LoginManager
import json
from functools import wraps
import sys
from flask_jwt_extended import JWTManager
from .login.models import User

#ACTIVE_ENDPOINTS = [('/',home), ('/dashboard', dashboard), ('/releases', releases), ('/artists', artists), ('/purchase', purchase), ("/products", products) ]
ACTIVE_ENDPOINTS = [('/',home),('/CIE',CIE), ('/token', token) ]

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

    SWAGGER_URL="/swagger"
    API_URL="/static/swagger.json"

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'Access API'
        }
    )
    app.config["JWT_SECRET_KEY"] = "holaMundo" 
    jwt = JWTManager(app)
    #app.config['SERVER_NAME'] = 'localhost:5000'

    app.config['SECRET_KEY'] = 'secret'
    app.config['DEBUG'] = True

    # Setup LDAP Configuration Variables. Change these to your own settings.
    # All configuration directives can be found in the documentation.

    # Hostname of your LDAP Server
    app.config['LDAP_HOST'] = 'ad.mydomain.com'

    # Base DN of your directory
    app.config['LDAP_BASE_DN'] = 'dc=mydomain,dc=com'

    # Users DN to be prepended to the Base DN
    app.config['LDAP_USER_DN'] = 'ou=users'

    # Groups DN to be prepended to the Base DN
    app.config['LDAP_GROUP_DN'] = 'ou=groups'

    # The RDN attribute for your user schema on LDAP
    app.config['LDAP_USER_RDN_ATTR'] = 'cn'

    # The Attribute you want users to authenticate to LDAP with.
    app.config['LDAP_USER_LOGIN_ATTR'] = 'mail'

    # The Username to bind to LDAP with
    app.config['LDAP_BIND_USER_DN'] = None

    # The Password to bind to LDAP with
    app.config['LDAP_BIND_USER_PASSWORD'] = None

                  # Setup a Flask-Login Manager
    ldap_manager = LDAP3LoginManager(app)          # Setup a LDAP3 Login Manager.
    
    
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





