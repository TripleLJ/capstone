from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, AnyOf, URL


class TeamForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )

    image = StringField(
        'image', validators=[DataRequired()]
    )

    color1 = StringField(
        'color1', validators=[DataRequired()]
    )

    color2 = StringField(
        'color2', validators=[DataRequired()]
    )




class PlayerForm(FlaskForm):
    first_name = StringField(
        'first_name', validators=[DataRequired()]
    )

    last_name = StringField(
        'last_name', validators=[DataRequired()]
    )

    number = StringField(
        'number', validators=[DataRequired()]
    )
    # Number is a string to allow instances like #00, #09, #0, #9, etc.

    image = StringField(
        'image', validators=[DataRequired()]
    )

    position = StringField(
        'position', validators=[DataRequired()]
    )

    team_id = IntegerField(
        'team_id', validators=[DataRequired()]
    )
