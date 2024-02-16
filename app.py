'''Description: This is the main file for the Flask application.'''

from flask import Flask, jsonify, request
from search import scrap_fmoviesz_by_name

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    '''Return the home page.'''
    routes = get_routes()
    return jsonify(routes)


def handle_error(e):
    '''note that we set the status explicitly'''
    return jsonify(error=str(e)), e.code


def get_routes():
    '''Return a dictionary of all routes and their methods.'''
    return {
        str(rule): str(rule.methods)
        for rule in app.url_map.iter_rules()
        if rule.endpoint != 'static'
    }, 200


@app.route('/media/searchByName', methods=['GET'])
def search_media():
    '''Search for media by title.'''
    name = request.args.get('name', default='')
    if not name:
        return jsonify({'error': 'Keyword is required'}), 400
    media = scrap_fmoviesz_by_name(name)
    return jsonify(media), 200


app.register_error_handler(404, handle_error)
app.register_error_handler(500, handle_error)


if __name__ == '__main__':
    app.run()
