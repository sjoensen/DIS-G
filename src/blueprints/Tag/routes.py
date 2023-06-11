from flask import Blueprint, render_template
from src.forms import TagForm
from src.queries import get_tags

Tag = Blueprint('tag', __name__)

TABLE_COLUMNS = [
    ("type", "Name"),
]


@Tag.route("/tags/")
def tags():
    table_data = get_tags()
    form = TagForm()
    return render_template("pages/search.html", form=form, columns=TABLE_COLUMNS, table_data=table_data)
