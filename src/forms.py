from src.queries import get_tags, get_stations, get_lines
from flask_wtf import FlaskForm
from wtforms import widgets, StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, \
    SelectMultipleField, HiddenField
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
    submit = SubmitField('Search')
    line = SelectField("Line")
    origin = SelectField("Origin")
    destination = SelectField("Destination")
    # search_type = SelectField("Search type")
    specials = SelectField("Sorting")
    min_walk_minutes = IntegerField("Min walk time, in minutes")
    max_walk_minutes = IntegerField("Max walk time, in minutes")
    min_line_proximity = IntegerField("Min amount of stops")
    max_line_proximity = IntegerField("Max amount of stops")
    tags = MultiCheckboxField("Tag")


class TagForm(FlaskForm):
    add = SubmitField("Add")
    edit = SubmitField("Update")
    # add = SubmitField("Add")
    type = StringField("Name")
    old_type = StringField("Old_Type")


class LocationForm(FlaskForm):
    id = IntegerField("ID")
    name = StringField("Name")
    address = StringField("Address")
    station = StringField("Station")
    minutes_to_walk = IntegerField("Minutes to walk")


class LineForm(FlaskForm):
    name = StringField("Name")
    length = IntegerField("Length")


class AmenityForm(FlaskForm):
    id = IntegerField("ID")
    name = StringField("Name")


class StationForm(FlaskForm):
    name = StringField("Name")
    area = StringField("Area")
