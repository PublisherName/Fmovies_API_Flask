from .parser import HtmlParser
from .settings import FM_URL


class fmoviesScraper(HtmlParser):
    def __init__(self) -> None:
        pass

    def by_trending(self) -> dict:
        url = f"{FM_URL}/trending"
        return self.get_media(url)

    def by_recommendation(self) -> dict:
        url = f"{FM_URL}/home"
        return self.get_media(url, ["movies", "shows"])

    def by_name(self, name: str) -> dict:
        url = f"{FM_URL}/filter?keyword={name}"
        return self.get_media(url)
