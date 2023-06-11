from flask import render_template, request, Blueprint

from src.forms import SearchForm
from src.queries import get_tags, get_lines, get_stations, filtered_search

Home = Blueprint('home', __name__)

SPECIAL_SEARCH_MIN_WALK = 0
SPECIAL_SEARCH_MAX_WALK = 1
SPECIAL_SEARCH_MIN_LINE_PROXIMITY = 2
SPECIAL_SEARCH_MAX_LINE_PROXIMITY = 3

SPECIAL_CHOICES = [
    (("proximity", "ASC"), "Closest to origin"),
    (("proximity", "DESC"), "Furthest from origin"),
    (("minutes_to_walk", "ASC"), "Minimum walk time"),
    (("minutes_to_walk", "DESC"), "Maximum walk time"),
]


@Home.route("/", methods=['GET', 'POST'])
@Home.route("/search", methods=['GET', 'POST'])
def search():
    results = []
    form = SearchForm()
    form.line.choices = [(l.name, l.name) for l in get_lines()]
    stations = get_stations()
    form.origin.choices = [(s.name, s.name) for s in stations]
    form.destination.choices = [("destination_none","None")] + [("destination_all", "All")] + [(s.name, s.name) for s in stations]
    form.tags.choices = [(t.type, t.type) for t in get_tags()]
    form.specials.choices = SPECIAL_CHOICES

    if request.method == 'POST':
        results = filtered_search(
            form.line.data,
            form.origin.data,
            form.destination.data,
            form.tags.data,
            form.min_walk_minutes.data,
            form.max_walk_minutes.data,
            form.min_line_proximity.data,
            form.max_line_proximity.data,
            form.specials.data
        )

    return render_template("pages/search.html", form=form, results=results)
