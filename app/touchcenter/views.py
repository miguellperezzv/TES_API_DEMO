from flask import Blueprint, Response, flash, session, request, g, render_template, redirect, url_for, jsonify, make_response


home = Blueprint('home', __name__)


@home.route("/")
def index():
    return render_template("home.html") 