from flask import Blueprint, Response, flash, session, request, g, render_template, redirect, url_for, jsonify, make_response, current_app
from flask_jwt_extended import create_access_token
from ldap3 import Server, Connection, ALL

import os

token = Blueprint('token', __name__, url_prefix = '/token')

    

@token.route("/", methods=["POST"])
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


def login_AD(usr, pwd):
    # import class and constants

# define the server
    s = Server('english.local', get_info=ALL)  # define an unsecure LDAP server, requesting info on DSE and schema

    # define the connection
    c = Connection(s, user='english\\'+usr, password=pwd)
    c.bind()
    print(c.result)
    return c.result





