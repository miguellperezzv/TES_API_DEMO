from .config import DevelopmentConfig
from flask import Flask, session
#from db import db, ma 
from .CIE.views import CIE, home
from flask_swagger_ui import get_swaggerui_blueprint
import json


#ACTIVE_ENDPOINTS = [('/',home), ('/dashboard', dashboard), ('/releases', releases), ('/artists', artists), ('/purchase', purchase), ("/products", products) ]
ACTIVE_ENDPOINTS = [('/',home),('/CIE',CIE) ]



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
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


    return app




if __name__ == "__main__":
    app_flask = create_app()


    print("DEBUG" + str(app_flask.debug))
    app_flask.run()