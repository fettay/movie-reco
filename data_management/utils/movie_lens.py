from urllib.parse import quote
import logging
from difflib import SequenceMatcher

import pandas as pd
import numpy as np
import requests
from retry import retry

from data_management.utils.proxies import get_random_proxy


AUTOCOMPLETE_URL = "https://movielens.org/api/searches/omni/%s"
LOGIN_URL = "https://movielens.org/api/sessions"
SIMILAR_URL = "https://movielens.org/api/movies/%d/similar?num=24&page=1&critique=&includeDefaultTags=true"


class MovieLensApi:
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._cookies = None
    
    def _login(self):
        response = requests.post(LOGIN_URL, json=dict(userName=self._username, password=self._password))
        self._cookies = response.cookies.get_dict()
        return response.status_code

    def _autocomplete(self, movie_name, proxies):
        if self._cookies is None:
            self._login()
        movie_name = quote(movie_name.split("(")[0]) # Remove year info
        response = requests.get(AUTOCOMPLETE_URL % movie_name, cookies=self._cookies, proxies=proxies)

        if response.status_code != 200:
            logging.warning("Error fetching data for %s" % movie_name)
    
        data = response.json()
        result = data['data']['movieViewModel']['payload']

        if len(result) == 0:
            logging.warning("No recommandation found for %s" % movie_name)
        return result

    def _find_id(self, movie_name, proxies):
        possibles = self._autocomplete(movie_name, proxies)
        values = np.array([-SequenceMatcher(None, m['label'], movie_name).ratio() for m in possibles])
        arg_sorted = np.argsort(values)
        return possibles[arg_sorted[0]]['movieId']
    
    def _query_movie_id(self, movie_id, proxies):
        if self._cookies is None:
            self._login()
        response = requests.get(SIMILAR_URL % movie_id, cookies=self._cookies, proxies=proxies)
        if response.status_code != 200:
            return None
        return self._format_movie_res(response.json())

    def _match_movie_reco_with_ids(self, collection, movies):
        if movies is None:
            return None
        movies_ids = [collection.find_one({"title": m}) for m in movies]
        return [movie['_id'] for movie in movies_ids if movie is not None]
    
    @staticmethod
    def _format_movie_res(result):
        return [str(m['movie']['title']) for m in result['data']['similarMovies']['searchResults']]

    @retry(tries=5)
    def run(self, movie_name, collection):
        proxies = None
        movie_id = self._find_id(movie_name, proxies)
        if movie_id is None:
            return {'movie_lens_recos': None}
        
        movies = self._query_movie_id(movie_id, proxies)
        if movies is None:
            return {'movie_lens_recos': None}
        
        return {'movie_lens_recos': self._match_movie_reco_with_ids(collection, movies)}


if __name__ == "__main__":
    from data_management.mongo_utils import get_collection
    api = MovieLensApi('mfettaya@hotmail.com', 'zxczxczxc')
    print(api.run("Infrared", get_collection()))