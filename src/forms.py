from src.queries import get_tags, get_stations, get_lines
from flask_wtf import FlaskForm
from wtforms import widgets, StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, \
    SelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


class LookupForm(FlaskForm):
    testB = BooleanField('Test')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SearchForm(FlaskForm):
    tags = MultiCheckboxField("Tags")
    line = SelectField("Line")
    origin = SelectField("Origin")
    destination = SelectField("Destination (optional)")
    submit = SubmitField('Search')
