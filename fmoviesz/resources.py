'''Resources module'''

from flask_restful import Resource
from flask import request, current_app

from .scraper import scrap_fmoviesz_by_name


class Home(Resource):
    '''This class represents the home page endpoint.'''

    def get(self):
        '''Return the home page.'''
        routes = self.get_routes()
        return routes, 200

    def get_routes(self):
        '''Return a dictionary of all routes and their methods.'''
        return {
            str(rule): str(rule.methods)
            for rule in current_app.url_map.iter_rules()
            if rule.endpoint != 'static'
        }, 200


class SearchMediaByName(Resource):
    ''' This class represents the search by name endpoint.'''

    def get(self):
        '''Search for media by title.'''
        name = request.args.get('name', default='')
        if not name:
            return {'error': 'name is required'}, 400
        media = scrap_fmoviesz_by_name(name)
        return media, 200
