from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import requests
import os
from flask_bootstrap import Bootstrap

app = Flask(__name__)  # Create a Flask app instance
Bootstrap(app)

@app.route('/')  # Define a route for the root URL ('/')
def index():
    pokemon_data = requests.get(f'https://pokeapi.co/api/v2/pokemon/?limit=-1').json()["results"]
    pokemon = []
    for item in pokemon_data:
        name = " ".join(item["name"].split("-")).title()
        sprite_id = item["url"].split("/")[-2]
        sprite_url = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{sprite_id}.png'  # Extract ID from the URL
        pokemon.append((name, sprite_url))

    return render_template('index.html', pokemon=pokemon)

@app.route('/get_pokemon', methods=['POST'])
def get_pokemon():
    try:
        pokemon = request.form['pokemon']
        pk = "-".join(pokemon.split(" ")).lower()
        return redirect(url_for('pokemon', pokemon=pk))
    except:
        return redirect(url_for('index'))

@app.route('/<pokemon>')
def pokemon(pokemon):
    try: 
        print(f'pokemon: {pokemon}')
        req = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}').json()

        pokemon_id = req.get(id)
        stats = req.get('stats', [])
        types = req.get('types', [])
        sprites = [req['sprites'].get(i) for i in req['sprites'] if req['sprites'].get(i)]
        if 'name' in req:
            name = " ".join(req['name'].split("-")).title()
        else:
            name = "Unknown"
        weight = req.get('weight', 0)

        # try: 
        #     sprites[0], sprites[1], sprites[2], sprites[3], sprites[4], sprites[5], sprites[6], sprites[7] = sprites[4], sprites[0], sprites[5], sprites[1], sprites[6], sprites[2], sprites[7], sprites[3]
        # except IndexError as e:
        #     print(f"Error: {e}")
        
        sprites = [i for i in sprites if i]

        return render_template('pokemon.html', 
                               id=pokemon_id,
                               stats=stats, 
                               types=types, 
                               sprites=sprites, 
                               name=name, 
                               weight=weight)
    except requests.exceptions.RequestException as e: 
        print(f'Error fetching pokemon: {e}')
        return redirect(url_for('index'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                            'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode (optional)