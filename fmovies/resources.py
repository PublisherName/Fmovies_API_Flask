from flask_restful import Resource
from flask import request, current_app

from .scraper import fmoviesScraper


class BaseMediaResource(Resource):
    def __init__(self) -> None:
        self.scraper = fmoviesScraper()

    def get_routes(self):
        return {
            f"{request.url_root[:-1]}{str(rule)}": str(rule.methods)
            for rule in current_app.url_map.iter_rules()
            if rule.endpoint != "static"
        }, 200


class Home(BaseMediaResource):
    def get(self):
        routes = self.get_routes()
        return routes, 200


class TrendingMedia(BaseMediaResource):
    def get(self):
        media = self.scraper.by_trending()
        return media, 200


class RecommendationMedia(BaseMediaResource):
    def get(self):
        """Get the recommendation media."""
        media = self.scraper.by_recommendation()
        return media, 200


class SearchMediaByName(BaseMediaResource):
    def get(self):
        name = request.args.get("name", default="").strip()
        if not name:
            return {"error": "name is required"}, 400
        media = self.scraper.by_name(name)
        return media, 200
