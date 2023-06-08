from src.db import util
from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = util.get_secret_key()

util.reset()


db_cursor = util.connect().cursor()


@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("pages/index.html")
