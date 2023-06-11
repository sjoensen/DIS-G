from flask import Blueprint, render_template

from src.forms import AmenityForm
from src.queries import get_amenities

Amenity = Blueprint('amenity', __name__)

TABLE_COLUMNS = [
    ("id", "ID", "data"),
    ("name", "Name", "data"),
]


@Amenity.route("/amenities/")
def amenities():
    table_data = get_amenities()
    form = AmenityForm()
    return render_template("pages/search.html", method="POST", action="home.search", form=form, columns=TABLE_COLUMNS, table_data=table_data)
