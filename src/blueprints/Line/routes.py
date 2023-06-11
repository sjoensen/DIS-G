from flask import Blueprint, render_template

from src.forms import LineForm
from src.queries import get_lines

Line = Blueprint('line', __name__)

TABLE_COLUMNS = [
    ("name", "Name", "data"),
    ("length", "Length", "data"),
]


@Line.route("/lines/")
def lines():
    table_data = get_lines()
    form = LineForm()
    return render_template("pages/search.html", method="POST", action="home.search", form=form, columns=TABLE_COLUMNS, table_data=table_data)
