# Fmovies API Using Flask

This is a basic fmovies api that allows you to search for movies and tv shows and get the links to watch them.

## Requirements

- Python 3.9
- pip
- gunicorn


## Installation 

    pip install -r requirements.txt

## Usage

    gunicorn --reload app:app

## Endpoints

    - /media/trending

    - /media/recommendation
    
    - /media/searchByName?name=<movie_name>