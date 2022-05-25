from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import requests as r


class SearchForm(FlaskForm):
    pokemon_name = StringField('Pokemon Name',
                           validators=[DataRequired()])
    submit = SubmitField('Search')
    
    def validate_pokemon_name(self,pokemon_name):
        data = r.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.data}')
        if data.status_code != 200:
            raise ValidationError('That Pokemon name was not found.')