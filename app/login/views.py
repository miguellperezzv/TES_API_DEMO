from flask import Blueprint, Response, flash, session, request, g, render_template, redirect, url_for, jsonify, make_response, current_app

from flask_jwt_extended import create_access_token
from authlib.integrations.flask_client import OAuth

from ldap3 import Server, Connection, ALL
import os


login = Blueprint('login', __name__ , url_prefix = '/login')
token = Blueprint('token', __name__)
oauth = OAuth(current_app)


@login.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        # validate input
        is_validated = validate_email_and_password(data.get('email'), data.get('password'))
        if is_validated is not True:
            return dict(message='Invalid data', data=None, error=is_validated), 400
        user = User().login(
            data["email"],
            data["password"]
        )
        if user:
            try:
                # token should expire after 24 hrs
                user["token"] = jwt.encode(
                    {"user_id": user["_id"]},
                    login.config["SECRET_KEY"],
                    algorithm="HS256"
                )
                return {
                    "message": "Successfully fetched auth token",
                    "data": user
                }
            except Exception as e:
                return {
                    "error": "Something went wrong",
                    "message": str(e)
                }, 500
        return {
            "message": "Error fetching auth token!, invalid email or password",
            "data": None,
            "error": "Unauthorized"
        }, 404
    except Exception as e:
        return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": None
        }, 500
    

@token.route("/token", methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    # Query your database for username and password
    #user = User.query.filter_by(username=username, password=password).first()
    result = login_AD(username,password)
    print("result descr ", result['description'])
    if result['description'] != 'success':
        # the user was not found on the database
        return jsonify({"msg": "Bad username or password"}), 401
    
    # create a new token with the user id inside
    access_token = create_access_token(identity=username)
    return jsonify({ "token": access_token, "user_id": username })

@token.route('/google/')
def googleSETTINGS():
   
    # Google Oauth Config
    # Get client_id and client_secret from environment variables
    # For developement purpose you can directly put it
    # here inside double quotes
    #GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    #GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

    GOOGLE_CLIENT_ID = '887753690694-1q1tc9o599qt8n9je0e0qv4iqa1ea0go.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = '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'
     
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
     
    # Redirect to google_auth function
    redirect_uri = url_for('token.google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)
 
@token.route('/google/auth/')
def google_auth():
    token_str = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token_str)
    print(" Google User ", user)
    return redirect('/')


def login_AD(usr, pwd):
    # import class and constants


# define the server
    s = Server('english.local', get_info=ALL)  # define an unsecure LDAP server, requesting info on DSE and schema

    # define the connection
    c = Connection(s, user='english\\'+usr, password=pwd)
    c.bind()
    print(c.result)
    return c.result
