from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class EnterPokemonForm(FlaskForm):
    pokemon_name = StringField('Enter Pokemon')
    submit = SubmitField('Submit')