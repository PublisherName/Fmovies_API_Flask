'''Parser Helper Module'''

from bs4 import BeautifulSoup
import requests
from .settings import FM_URL


class HtmlParser:
    '''HTML Parser helper class'''

    @staticmethod
    def get_html(url: str) -> str:
        '''Get the HTML content of the specified URL.'''
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            return {'error': str(e)}

    @staticmethod
    def parse_html(html: str) -> list:
        '''Parse the HTML content and return the movie divs.'''
        try:
            soup = BeautifulSoup(html, 'html.parser')
            return soup.find_all('div', class_='item')
        except (BeautifulSoup.FeatureNotFound, AttributeError) as e:
            return {'error': str(e)}

    @staticmethod
    def create_media_dict_from_div(div) -> dict:
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

    @staticmethod
    def get_media(url: str) -> dict:
        '''Get the list of media from the specified URL.'''
        html = HtmlParser.get_html(url)
        if 'error' in html:
            return html
        movie_divs = HtmlParser.parse_html(html)
        if 'error' in movie_divs:
            return movie_divs
        return {'media': [HtmlParser.create_media_dict_from_div(div) for div in movie_divs]}
