from flask import Blueprint, Response, flash, session, request, g, render_template, redirect, url_for, jsonify, make_response, current_app, abort
from flask_jwt_extended import create_access_token, verify_jwt_in_request, get_jwt
from ldap3 import Server, Connection, ALL
from functools import wraps
import jwt

from flask import current_app

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
    return jsonify({ "access_token": access_token, "user_id": username })






def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
       
        token = None
        print(request.headers["Authorization"])
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
            print(token)
        if not token:
            print("No hay token")
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            print("Estoy en el try")
            data=jwt.decode(token, "holaMundo", algorithms=["HS256"])
            
            current_user=validateUserAD(data["sub"])
            print(current_user)
            if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401

            

            #if not current_user["active"]:
             #   abort(403)
        except Exception as e:
            print("EXCEPCION " ,e)
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        #return f(current_user, *args, **kwargs)
        return f( *args, **kwargs)

    return decorated


def login_AD(usr, pwd):
    # import class and constants

    # define the server
    s = Server('english.local', get_info=ALL)  # define an unsecure LDAP server, requesting info on DSE and schema

    # define the connection
    c = Connection(s, user='english\\'+usr, password=pwd)
    c.bind()
    #c.search()

    print(c.result)
    return c.result

def validateUserAD(usr):

    try:
        s = Server('english.local', get_info=ALL)  # define an unsecure LDAP server, requesting info on DSE and schema

        # define the connection
        c = Connection(s, user='english\\developer', password='G2a0g2a00407')
        search_base = 'dc=english,dc=local'  # Cambia esto por la base de búsqueda adecuada
        search_filter = '(sAMAccountName=' + usr + ')'  # Cambia esto según la estructura de tu directorio LDAP
        c.bind()
        c.search(search_base, search_filter, attributes=['cn'])

        if len(c.entries) > 0:
            print("El usuario existe en el directorio LDAP.")
            print("Nombre del usuario:", c.entries[0].cn.value)
            print(c.entries[0])
            return {"usuario": "developer" }
        else:
            print("El usuario NO existe en el directorio LDAP.")
            return None
    except Exception as e:
        print("error en validate user ",e)
        return None




