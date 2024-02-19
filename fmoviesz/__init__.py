''' This file is the entry point of the application. '''

from flask import Flask
from flask_restful import Api
from .resources import SearchMediaByName, Home, TrendingMedia, RecommendationMedia


def create_app():
    '''Create the application.'''

    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Home, '/')
    api.add_resource(TrendingMedia, '/media/trending')
    api.add_resource(RecommendationMedia, '/media/recommendation')
    api.add_resource(SearchMediaByName, '/media/searchByName')

    return app
