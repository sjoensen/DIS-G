from flask import Blueprint, render_template

from src.forms import LocationForm
from src.queries import get_locations

Location = Blueprint('location', __name__)

TABLE_COLUMNS = [
    ("id", "ID", "data"),
    ("name", "Name", "data"),
    ("address", "Address", "data"),
    ("station", "Station", "data"),
    ("minutes_to_walk", "Minutes to walk", "data"),
]


@Location.route("/locations/")
def locations():
    table_data = get_locations()
    form = LocationForm()
    return render_template("pages/search.html", method="POST", action="home.search", form=form, columns=TABLE_COLUMNS, table_data=table_data)
