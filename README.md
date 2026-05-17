# Fmovies API Using Flask

This is a basic fmovies api that allows you to search for movies and tv shows and get the links to watch them.

## Requirements

- Python 3.9
- uv
- gunicorn


## Installation 

```bash
uv sync
```

## Configuration

Copy the example env file and adjust the values:

```bash
cp .env.example .env
```

## Usage

```bash
uv run gunicorn --reload app:app
```

## Endpoints

    - /media/trending

    - /media/recommendation
    
    - /media/searchByName?name=<movie_name>