import requests
from django.conf import settings

BASE = getattr(settings, "TMDB_API_BASE_URL", "https://api.themoviedb.org/3/")
TOKEN = getattr(settings, "TMDB_READ_ACCESS_TOKEN", "")

def get_headers(tkn=TOKEN):
    if not tkn:
        raise RuntimeError("TMDB_READ_ACCESS_TOKEN não configurado (.env)")
    return {"Authorization": f"Bearer {tkn}", "accept": "application/json"}

def search_movie(query, page=1):
    url = f"{BASE}search/movie"
    r = requests.get(url, headers=get_headers(), params={"query": query, "page": page, "include_adult": "false", "language": "pt-BR"})
    r.raise_for_status()
    return r.json()

def movie_details(movie_id):
    url = f"{BASE}movie/{movie_id}"
    r = requests.get(url, headers=get_headers(), params={"language": "pt-BR"})
    r.raise_for_status()
    return r.json()

def movie_credits(movie_id):
    url = f"{BASE}movie/{movie_id}/credits"
    r = requests.get(url, headers=get_headers(), params={"language": "pt-BR"})
    r.raise_for_status()
    return r.json()

def watch_providers(movie_id):
    url = f"{BASE}movie/{movie_id}/watch/providers"
    r = requests.get(url, headers=get_headers())
    r.raise_for_status()
    return r.json()


def trending_movies(time_window="day", language="pt-BR"):
    url = f"{BASE}trending/movie/{time_window}"
    r = requests.get(url, headers=get_headers(), params={"language": language})
    r.raise_for_status()
    return r.json()


def now_playing_movies(language="pt-BR", region="BR", page=1):
    url = f"{BASE}movie/now_playing"
    params = {"language": language, "region": region, "page": page}
    r = requests.get(url, headers=get_headers(), params=params)
    r.raise_for_status()
    return r.json()
