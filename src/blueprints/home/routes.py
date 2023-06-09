from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

Home = Blueprint('/', __name__)


@Home.route("/login")
def login():
    return render_template("pages/index.html")


@Home.route("/about")
def about():
    return render_template("pages/index.html")
