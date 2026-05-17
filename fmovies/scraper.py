from .parser import HtmlParser


class fmoviesScraper:
    def by_trending(self) -> dict:
        return HtmlParser.get_media()

    def by_recommendation(self) -> dict:
        return HtmlParser.get_media(["latest movies", "latest tv-series"])

    def by_name(self, name: str) -> dict:
        return HtmlParser.get_search_media(name)
