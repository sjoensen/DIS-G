from src.queries import get_tags, get_stations, get_lines
from flask_wtf import FlaskForm
from wtforms import widgets, StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, \
    SelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


class LookupForm(FlaskForm):
    testB = BooleanField('Test')


class IntRangeField(IntegerField):
    widget = widgets.RangeInput()


class SearchResultsTable():
    widget = widgets.TableWidget()


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SearchForm(FlaskForm):
    tags = MultiCheckboxField("Tags")
    line = SelectField("Line")
    min_walk_minutes = IntegerField("Min walk time, in minutes")
    max_walk_minutes = IntegerField("Max walk time, in minutes")
    min_line_proximity = IntegerField("Min amount of stops")
    max_line_proximity = IntegerField("Max amount of stops")
    specials = SelectField("Sorting")
    search_results = SearchResultsTable()
    origin = SelectField("Origin")
    destination = SelectField("Destination")
    submit = SubmitField('Search')
