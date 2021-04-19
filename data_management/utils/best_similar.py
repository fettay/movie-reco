import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import quote
from difflib import SequenceMatcher
from typing import Dict
import logging

import numpy as np
import pymongo


AUTOCOMPLETE_URL = "https://bestsimilar.com/site/autocomplete?term={movie_str}"
MOVIE_PAGE_URL = "https://bestsimilar.com{movie_url}"
HEADERS = {"user-agent": "Chrome/89.0.4389.114"}

def _autocomplete(movie_name):
    
    data = {"term": movie_name}
    url = AUTOCOMPLETE_URL.format(movie_str=movie_name)
    return requests.post(url, data=data, headers=HEADERS).json()

def _find_link(movie_name):
    possibles = _autocomplete(movie_name)
   
    if 'movie' not in possibles:
        return None
    
    values = np.array([-SequenceMatcher(None, m['label'], movie_name).ratio() for m in possibles['movie']])
    arg_sorted = np.argsort(values)
    return possibles['movie'][arg_sorted[0]]

def _get_themes_reco(bs):
    themes = bs.find(attrs={"class":"attr-tag-group-1"})
    clean_themes = list(themes.children)[-2].get_text().strip()
    clean_themes = clean_themes.replace("...", "").replace(" ", "")
    return clean_themes.split(",")

def _get_movie_names_reco(bs):
    names = bs.find_all(attrs={"class":"name-c"})
    movies = []
    movies.append(list(names[0].children)[0].get_text())
    for name in names[1:]:
        movies.append(name.find_all(attrs={"class":"name"})[0].get_text())
    return movies

def _match_movie_reco_with_ids(collection, movies):
    if movies is None:
        return None
    movies_ids = [collection.find_one({"title": m}) for m in movies]
    return [movie['_id'] for movie in movies_ids if movie is not None]


def get_movie_data(collection: pymongo.collection.Collection, movie: 'Movie') -> Dict:
    """Retrieve best similar movie data

    Args:
        collection (pymongo.collection.Collection): The main movie collection
        movie (Movie): Movie Object to enrich

    Returns:
        Dict: ExtraData for the Movie Object
    """
    empty_result = {'best_similar_themes': None, 'best_similar_recos': None}
    
    movie_name = movie.title
    movie_link = _find_link(movie_name)
    
    if movie_link is None:
        return empty_result
    
    response = requests.get(MOVIE_PAGE_URL.format(movie_url=movie_link['url']), headers=HEADERS)

    if response.status_code != 200:
        return empty_result
    
    bs = BeautifulSoup(response.content, 'html.parser')
    
    try:
        themes = _get_themes_reco(bs)
    except Exception:
        logging.warning("error themes for %s" % movie.title)
        themes = None
        
    try:
        recos = _get_movie_names_reco(bs)
    except IndentationError:
        logging.warning("error movie reco for %s" % movie.title)
        recos = None
    
    recos_ids = _match_movie_reco_with_ids(collection, recos)
    return {'best_similar_themes': themes, 'best_similar_recos': recos_ids}
    