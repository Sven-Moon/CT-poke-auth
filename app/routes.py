from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from app import app
from app.forms import SearchForm
import requests as r
from pokedex import Pokedex, Pokemon

pokedex = Pokedex()

@app.route('/')
def home():
 
    return render_template('home.html')

@app.route('/explorer', methods=['GET','POST'])
def explorer():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('display', pokemon_name=form.pokemon_name.data))
    
    if form.errors:
        flash(f'You have to add a name before pressing this button.', category='danger') 
        
    
        
    return render_template('explorer.html', title='Explorer',form=form)

@app.route('/explorer/<string:pokemon_name>')
@login_required
def display(pokemon_name):
    pokemon = pokedex.get_pokemon(pokemon_name)
    abilities = [pokedex.get_ability(ability_name) for ability_name in pokemon.abilities]
    return render_template('display.html', pokemon=pokemon,abilities=abilities)