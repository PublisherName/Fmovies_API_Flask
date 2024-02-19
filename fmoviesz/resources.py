'''Resources module'''

from flask_restful import Resource
from flask import request, current_app

from .scraper import FmovieszScraper


class BaseMediaResource(Resource):
    '''Base class for media resources.'''

    def __init__(self) -> None:
        self.scraper = FmovieszScraper()

    def get_routes(self):
        '''Return a dictionary of all routes and their methods.'''
        return {
            f"{request.url_root[:-1]}{str(rule)}": str(rule.methods)
            for rule in current_app.url_map.iter_rules()
            if rule.endpoint != 'static'
        }, 200


class Home(BaseMediaResource):
    '''This class represents the home page endpoint.'''

    def get(self):
        '''Return the home page.'''
        routes = self.get_routes()
        return routes, 200


class TrendingMedia(BaseMediaResource):
    ''' This class represents the trending media endpoint.'''

    def get(self):
        '''Get the trending media.'''
        media = self.scraper.by_trending()
        return media, 200


class RecommendationMedia(BaseMediaResource):
    ''' This class represents the recommendation media endpoint.'''

    def get(self):
        '''Get the recommendation media.'''
        media = self.scraper.by_recommendation()
        return media, 200


class SearchMediaByName(BaseMediaResource):
    ''' This class represents the search by name endpoint.'''

    def get(self):
        '''Search for media by title.'''
        name = request.args.get('name', default='').strip()
        if not name:
            return {'error': 'name is required'}, 400
        media = self.scraper.by_name(name)
        return media, 200
