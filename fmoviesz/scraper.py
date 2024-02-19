'''Scraper module'''

from .parser import HtmlParser
from .settings import FM_URL


class FmovieszScraper(HtmlParser):
    ''' Fmoviesz scrapper class '''

    def __init__(self) -> None:
        pass

    def by_trending(self) -> dict:
        '''Get the list of medias from fmoviesz.to based on the trends.'''
        url = f"{FM_URL}/trending"
        return self.get_media(url)

    def by_recommendation(self) -> dict:
        '''Get the list of medias from fmoviesz.to based on the recommendation.'''
        url = f"{FM_URL}/home"
        return self.get_media(url)

    def by_name(self, name: str) -> dict:
        '''Get the list of medias from fmoviesz.to based on the movie name.'''
        url = f"{FM_URL}/filter?keyword={name}"
        return self.get_media(url)
