from flask_restful import Resource
from flask import request, current_app

from .scraper import fmoviesScraper

_scraper = fmoviesScraper()


class Home(Resource):
    def get(self):
        routes = {
            f"{request.url_root[:-1]}{rule}": str(rule.methods)
            for rule in current_app.url_map.iter_rules()
            if rule.endpoint != "static"
        }
        return routes, 200


class TrendingMedia(Resource):
    def get(self):
        result = _scraper.by_trending()
        status = 200 if "media" in result else 502
        return result, status


class RecommendationMedia(Resource):
    def get(self):
        result = _scraper.by_recommendation()
        status = 200 if "media" in result else 502
        return result, status


class SearchMediaByName(Resource):
    def get(self):
        name = request.args.get("name", default="").strip()
        if not name:
            return {"error": "name is required"}, 400
        result = _scraper.by_name(name)
        status = 200 if "media" in result else 502
        return result, status
