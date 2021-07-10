from app import models
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class AddChipsForm(FlaskForm):
    name = StringField('Name')
    chips = IntegerField('Chips')
    submit = SubmitField('Submit')