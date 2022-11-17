from flask import Flask, request, render_template
import json
import requests

app = Flask(__name__)

@app.route('/')
def homepage():
    """A homepage with handy links for your convenience."""
    return render_template('form.html')

SWAPI_API_URL = "https://swapi.py4e.com/api/"

@app.route("/result")
def search():
    """Show a form to search for info from Swapi API."""
    character_id = request.args.get("character_id")
    response_people = requests.get(SWAPI_API_URL + "people/" + character_id)
    character = json.loads(response_people.content)
    response_films = list()
    try:
        films = character["films"]
        response_films = list()
        for film in films:
            response_films.append(json.loads(requests.get(film).content))
    except KeyError:
        response_films = ""

    try:
        response_homeworld = requests.get(character["homeworld"])
        homeworld = json.loads(response_homeworld.content)
    except KeyError:
        homeworld = ""
    context = {
        'character': character, 
        'films': response_films,
        'homeworld': homeworld
    }
    return render_template('result.html', **context)

if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
