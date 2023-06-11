from flask import render_template, request, Blueprint

from src.forms import SearchForm
from src.queries import get_tags, get_lines, get_stations, filtered_search, find_highest_tag_incidence, \
    get_stations_with_all_tags

Home = Blueprint('home', __name__)

SPECIAL_SEARCH_MIN_WALK = 0
SPECIAL_SEARCH_MAX_WALK = 1
SPECIAL_SEARCH_MIN_LINE_PROXIMITY = 2
SPECIAL_SEARCH_MAX_LINE_PROXIMITY = 3

SPECIAL_CHOICES = [
    ("proximity ASC, minutes_to_walk ASC", "Closest to origin"),
    ("proximity DESC, minutes_to_walk ASC", "Furthest from origin"),
    ("minutes_to_walk ASC, proximity ASC", "Minimum walk time"),
    ("minutes_to_walk DESC, proximity ASC", "Maximum walk time"),
]

TABLE_COLUMNS = [
    ("station", "Station", "data"),
    ("minutes_to_walk", "Minutes to walk", "data"),
    ("name", "Name", "data"),
    ("address", "Address", "data"),
    ("tag", "Tag", "data"),
]

SEARCH_TYPE_CHOICES = [
    ("ANY_TAGS_MATCHING", "Match any tags"),
    ("ALL_TAGS_MATCHING", "Match all tags"),
    ("HIGHEST_INCIDENCE", "Most tag hits"),
]


@Home.route("/", methods=['GET', 'POST'])
@Home.route("/search", methods=['GET', 'POST'])
def search():
    results = []
    form = SearchForm()
    form.line.choices = [(l.name, l.name) for l in get_lines()]
    stations = get_stations()
    form.origin.choices = [(s.name, s.name) for s in stations]
    form.destination.choices = [("destination_all", "All")] + [("destination_none","None")] + [(s.name, s.name) for s in stations]
    form.tags.choices = [(t.type, t.type) for t in get_tags()]
    form.specials.choices = SPECIAL_CHOICES
    # form.search_type.choices = SEARCH_TYPE_CHOICES

    min_minutes_to_walk = form.min_walk_minutes.data
    min_minutes_to_walk = 0 if min_minutes_to_walk is None else min_minutes_to_walk

    max_minutes_to_walk = form.max_walk_minutes.data
    max_minutes_to_walk = 10000 if max_minutes_to_walk is None else max_minutes_to_walk

    min_line_proximity = form.min_line_proximity.data
    min_line_proximity = 0 if min_line_proximity is None else min_line_proximity

    max_line_proximity = form.max_line_proximity.data
    max_line_proximity = 10000 if max_line_proximity is None else max_line_proximity
    sorting = form.specials.data

    if request.method == "POST":
        results = filtered_search(
            form.line.data,
            form.origin.data,
            form.destination.data,
            form.tags.data,
            min_minutes_to_walk,
            max_minutes_to_walk,
            min_line_proximity,
            max_line_proximity,
            sorting
        )

    # if form.search_type.data == 'ANY_TAGS_MATCHING':
    # elif form.search_type.data == 'ALL_TAGS_MATCHING':
    #     results = get_stations_with_all_tags(
    #         form.line.data,
    #         form.origin.data,
    #         form.destination.data,
    #         form.tags.data,
    #         min_minutes_to_walk,
    #         max_minutes_to_walk,
    #         min_line_proximity,
    #         max_line_proximity,
    #         sorting
    #     )
    # elif form.search_type.data == 'HIGHEST_INCIDENCE':
    #     results = find_highest_tag_incidence(
    #         form.line.data,
    #         form.origin.data,
    #         form.destination.data,
    #         form.tags.data,
    #         min_minutes_to_walk,
    #         max_minutes_to_walk
    #     )

    return render_template("pages/search.html", method="POST", action="home.search", form=form, table_data=results, columns=TABLE_COLUMNS)


@Home.route("/about/")
def about():
    return render_template("pages/about.html")


@Home.route("/map/")
def show_map():
    return render_template("pages/map.html")
