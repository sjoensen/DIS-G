from flask import render_template, request, Blueprint

from src.forms import SearchForm
from src.queries import get_tags, get_lines, get_stations, get_locations, get_locations_with_tags

Home = Blueprint('home', __name__)


@Home.route("/", methods=['GET', 'POST'])
@Home.route("/search", methods=['GET', 'POST'])
def search():
    results = []
    form = SearchForm()
    form.line.choices = [(l.name, l.name) for l in get_lines()]
    stations = get_stations()
    form.origin.choices = [(s.name, s.name) for s in stations]
    form.destination.choices = [("","Ingen")] + [(s.name, s.name) for s in stations]
    form.tags.choices = [(t.type, t.type) for t in get_tags()]

    if request.method == 'POST':
        results = get_stations_with_all_tags(
            form.line.data,
            form.origin.data,
            form.destination.data,
            form.tags.data
        )

    return render_template("pages/search.html", form=form, results=results)
