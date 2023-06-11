from src.db import util
from src import queries
from flask import Flask
from src.queries import test
from src.blueprints.Home.routes import Home


app = Flask(__name__)
app.config['SECRET_KEY'] = util.get_secret_key()

util.reset()
test()

app.register_blueprint(Home)
