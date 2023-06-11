from flask import Blueprint, render_template, redirect, url_for, request
from src.forms import TagForm
from src.queries import get_tags, delete

Tag = Blueprint('tag', __name__)

TABLE_COLUMNS = [
    ("type", "Name", "data"),
    ("asd", "", "edit"),
    ("tag.delete_tag", "", "delete"),
]


@Tag.route("/tags/")
def tags():
    table_data = get_tags()
    form = TagForm()
    return render_template("pages/search.html", method="POST", action="home.search", form=form, columns=TABLE_COLUMNS, table_data=table_data)


@Tag.route("/tag/<type>", methods=["POST"])
def delete_tag(type):
    print(type)
    delete("tags", "type", [type])
    return redirect(url_for("tag.tags"))