from flask import Blueprint, render_template

from src.forms import StationForm
from src.queries import get_stations

Station = Blueprint('station', __name__)

TABLE_COLUMNS = [
    ("name", "Name", "data"),
    ("area", "Area", "data"),
]


@Station.route("/stations/")
def stations():
    table_data = get_stations()
    form = StationForm()
    return render_template("pages/search.html", method="POST", action="home.search", form=form, columns=TABLE_COLUMNS, table_data=table_data)
