from flask import Blueprint, render_template, redirect, url_for

from src.forms import StationForm
from src.queries import get_stations, delete

Station = Blueprint('station', __name__)

TABLE_COLUMNS = [
    ("name", "Name", "data"),
    ("area", "Area", "data"),
]


@Station.route("/stations/")
def stations():
    table_data = get_stations()
    form = StationForm()
    return render_template("pages/stations.html", method="POST", action="station.stations", form=form, columns=TABLE_COLUMNS, table_data=table_data)


@Station.route("/station/<name>", methods=["POST"])
def delete_station(name):
    print(type)
    delete("stations", "name", [name])
    return redirect(url_for("station.stations"))
