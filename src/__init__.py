from src.blueprints.Amenity.routes import Amenity
from src.blueprints.Line.routes import Line
from src.blueprints.Location.routes import Location
from src.blueprints.Station.routes import Station
from src.blueprints.Tag.routes import Tag
from src.db import util
from src import queries
from flask import Flask

from src.queries import test
from src.blueprints.Home.routes import Home


app = Flask(__name__)
app.config['SECRET_KEY'] = util.get_secret_key()

util.reset()
test()

app.register_blueprint(Tag)
app.register_blueprint(Location)
app.register_blueprint(Station)
app.register_blueprint(Amenity)
app.register_blueprint(Line)
app.register_blueprint(Home)
