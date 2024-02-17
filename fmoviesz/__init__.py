''' This file is the entry point of the application. '''

from flask import Flask
from flask_restful import Api
from .resources import SearchMediaByName, Home


def create_app():
    '''Create the application.'''

    app = Flask(__name__)
    api = Api(app)

    api.add_resource(SearchMediaByName, '/media/searchByName')
    api.add_resource(Home, '/')

    return app
