from src.db import util
from src import queries
from flask import Flask, render_template, redirect, url_for
from flask_login import current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = util.get_secret_key()

util.reset()


db_cursor = util.connect().cursor()


queries.test()


@app.before_request
def authenticate():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    # logic for verifying tokens
    pass


@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("pages/index.html")
