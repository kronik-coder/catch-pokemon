from flask import render_template, request
import requests
from .forms import EnterPokemonForm
from flask_login import login_required, current_user
from .import bp as main
from app.models import CatchPokemon

@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = EnterPokemonForm()
    if request.method == 'POST':
        pokemon_name = request.form.get('pokemon_name')
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
        response = requests.get(url)
        if response.ok:
            stats = {
                "name": response.json()["forms"][0]["name"],
                "hp": response.json()["stats"][0]["base_stat"],
                "defense": response.json()["stats"][2]["base_stat"],
                "attack": response.json()["stats"][1]["base_stat"],
                "shiny": response.json()["sprites"]["front_shiny"]
                }
            new_pokemon = CatchPokemon(user_id=current_user.id, pokemon_name=pokemon_name)
            new_pokemon.save()

            return render_template('search.html.j2', stats=stats, form=form)
    return render_template('search.html.j2', form=form)