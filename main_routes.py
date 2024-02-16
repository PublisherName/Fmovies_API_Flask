'''This module contains the main routes for the application.'''

from flask import Blueprint, jsonify, current_app

main_routes_bp = Blueprint('main_routes', __name__)


@main_routes_bp.route('/', methods=['GET'])
def home():
    '''Return the home page.'''
    routes = get_routes()
    return jsonify(routes)


def get_routes():
    '''Return a dictionary of all routes and their methods.'''
    return {
        str(rule): str(rule.methods)
        for rule in current_app.url_map.iter_rules()
        if rule.endpoint != 'static'
    }, 200
