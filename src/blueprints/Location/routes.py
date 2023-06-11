from flask import Blueprint, render_template

from src.forms import LocationForm
from src.queries import get_locations

Location = Blueprint('location', __name__)

TABLE_COLUMNS = [
    ("id", "ID"),
    ("name", "Name"),
    ("address", "Address"),
    ("station", "Station"),
    ("minutes_to_walk", "Minutes to walk"),
]


@Location.route("/locations/")
def locations():
    table_data = get_locations()
    form = LocationForm()
    return render_template("pages/search.html", form=form, columns=TABLE_COLUMNS, table_data=table_data)
