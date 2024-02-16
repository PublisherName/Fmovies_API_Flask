'''Description: This is the main file for the Flask application.'''

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    '''Return the home page.'''
    routes = get_routes()
    return jsonify(routes)


@app.route('/movies', methods=['GET'])
def get_movies():
    '''Return a list of movies'''
    return jsonify(response="Movies endpoint")


@app.route('/movies/search', methods=['GET', 'POST'])
def search_movies():
    '''Search for movies by title.'''
    return jsonify(reponse="Search movies endpoint")


def get_routes():
    '''Return a dictionary of all routes and their methods.'''
    return {
        str(rule): str(rule.methods)
        for rule in app.url_map.iter_rules()
        if rule.endpoint != 'static'
    }


if __name__ == '__main__':
    app.run()
