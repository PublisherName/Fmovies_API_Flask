'''Search module'''

import os
from dotenv import load_dotenv
from flask import Blueprint
import requests
from bs4 import BeautifulSoup

load_dotenv()

FM_URL = os.getenv('FM_URL')

search_by_name_bp = Blueprint('search_by_name', __name__)


def create_item(div) -> dict:
    '''Create a dictionary of the movie item.'''
    quality = div.find('div', class_='quality').text
    poster_div = div.find('div', class_='poster')
    poster = poster_div.find('img')['data-src']
    link = f"{FM_URL}" + poster_div.find('a')['href']
    title = div.find('div', class_='meta').find('a').text
    release_date = div.find('div', class_='meta').find('span').text
    type_span = div.find('div', class_='meta').find('span', class_='type')
    item_type = 'Series' if 'SS' in type_span.text else 'Movie'
    season = type_span.text.split(' ')[1] if item_type == 'Series' else None
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


def scrap_fmoviesz_by_name(name: str) -> dict:
    '''Get the list of movies from fmoviesz.to based on the movie name.'''
    url = f"{FM_URL}/filter?keyword={name}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return {'error': str(e)}

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        movie_divs = soup.find_all('div', class_='item')
    except (BeautifulSoup.FeatureNotFound, AttributeError) as e:
        return {'error': str(e)}

    return {'media': [create_item(div) for div in movie_divs]}
