from flask import Blueprint, render_template, redirect, url_for, request

from src.db.util import UniqueViolation
from src.forms import TagForm
from src.queries import get_tags, delete, insert_tag, update_tag

Tag = Blueprint('tag', __name__)

TABLE_COLUMNS = [
    ("type", "Name", "data"),
    ("", "", "edit"),
    ("", "", "delete"),
]


@Tag.route("/tags/")
def tags():
    table_data = get_tags()
    form = TagForm()
    return render_template("pages/tags.html", form=form, columns=TABLE_COLUMNS, table_data=table_data)


@Tag.route("/tag/<type>", methods=["POST"])
def delete_tag(type):
    try:
        delete("tags", "type", [type])
        return redirect(url_for("tag.tags"))
    except UniqueViolation as err:

        return redirect(url_for("tag.tags"))


@Tag.route("/tag/add", methods=["POST"])
def add_tag():
    form = TagForm()
    try:
        insert_tag(form.type.data)
        return redirect(url_for("tag.tags"))
    except UniqueViolation as err:
        pass
    return redirect(url_for("tag.tags"))


@Tag.route("/tag/edit/", methods=["POST"])
def edit_tag():
    form = TagForm()
    update_tag(form.type.data, form.old_type.data)
    table_data = get_tags()
    form.type.data = ""
    form.old_type.data = ""
    return render_template("pages/tags.html", form=form, columns=TABLE_COLUMNS, table_data=table_data)


@Tag.route("/tag/select/<type>", methods=["POST"])
def select_tag(type):
    table_data = get_tags()
    form = TagForm()
    form.type.data = type
    form.old_type.data = type
    return render_template("pages/selected-tags.html", form=form, columns=TABLE_COLUMNS, table_data=table_data)

