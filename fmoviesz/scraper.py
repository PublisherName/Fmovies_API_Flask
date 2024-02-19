'''Scraper module'''

import requests
from bs4 import BeautifulSoup
from .settings import FM_URL


class FmovieszScraper:
    ''' Fmoviesz scrapper class '''

    def __init__(self) -> None:
        pass

    def get_html(self, url: str) -> str:
        '''Get the HTML content of the specified URL.'''
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            return {'error': str(e)}

    def parse_html(self, html: str) -> list:
        '''Parse the HTML content and return the movie divs.'''
        try:
            soup = BeautifulSoup(html, 'html.parser')
            return soup.find_all('div', class_='item')
        except (BeautifulSoup.FeatureNotFound, AttributeError) as e:
            return {'error': str(e)}

    def create_media_dict_from_div(self, div) -> dict:
        '''Create a dictionary of the movie item.'''
        quality = div.find('div', class_='quality').text
        poster_div = div.find('div', class_='poster')
        poster = poster_div.find('img')['data-src']
        link = f"{FM_URL}" + poster_div.find('a')['href']
        title = div.find('div', class_='meta').find('a').text
        release_date = div.find('div', class_='meta').find('span').text
        type_span = div.find('div', class_='meta').find('span', class_='type')
        item_type = 'Series' if 'SS' in type_span.text else 'Movie'
        season = type_span.text.split(
            ' ')[1] if item_type == 'Series' else None
        episode = None

        if item_type == 'Series':
            episode = div.find('div', class_='meta').find_all('span')[-1].text

        return {
            'quality': quality,
            'poster': poster,
            'title': title,
            'release_date': release_date,
            'type': item_type,
            'season': season,
            'episode': episode,
            'link': link
        }

    def get_media(self, url: str) -> dict:
        '''Get the list of media from the specified URL.'''
        html = self.get_html(url)
        if 'error' in html:
            return html
        movie_divs = self.parse_html(html)
        if 'error' in movie_divs:
            return movie_divs
        return {'media': [self.create_media_dict_from_div(div) for div in movie_divs]}

    def by_name(self, name: str) -> dict:
        '''Get the list of medias from fmoviesz.to based on the movie name.'''
        url = f"{FM_URL}/filter?keyword={name}"
        return self.get_media(url)

    def by_trending(self) -> dict:
        '''Get the list of medias from fmoviesz.to based on the trends.'''
