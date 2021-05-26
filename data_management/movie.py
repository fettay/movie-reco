from typing import List
import logging
import os

from imdb import IMDb
from bson.objectid import ObjectId

from data_management.utils.best_similar import get_movie_data
from data_management.utils.movie_lens import MovieLensApi
from data_management.constants import RELEVANT_KEYS


class Movie:
    
    def __init__(self, imdbID: str, **kwargs):
        self.imdbID = imdbID
        for attr, v in kwargs.items():
            setattr(self, attr, v)

    def upload_to_mongo(self, db_connection, upsert=True):
        db_connection.update_one({'imdbID': self.imdbID}, {'$set': vars(self)}, upsert)
        logging.info("id movie {} saved to mongo DB".format(self.imdbID))
        return 0

    def enrich_from_imdb(self, fields, collection):
        ia = IMDb()
        imdb_movie = ia.get_movie(self.imdbID)
        update = {field: imdb_movie.data.get(field) for field in fields}
        collection.update_one({'imdbID': self.imdbID}, {'$set': update})
    
    def get(self, attr, default_val=None):
        if hasattr(self, attr):
            return getattr(self, attr)
        return default_val

    def select_plot(self):
        """return the closest plot to 1500 characters"""
        if hasattr(self, 'plot') and self.plot is not None:
            plot = [x.split('::')[0] for x in self.plot]
            lengths = [abs(len(x) - 1500) for x in plot]
            closest_plot = plot[plot.index(min(plot))]
        else:
            closest_plot = None
        return closest_plot

    @staticmethod
    def _load_imdb_data(imdbID: str) -> 'Movie':
        ia = IMDb()
        imdb_movie = ia.get_movie(imdbID)
        if len(imdb_movie) == 0:
            logging.warning('no movie with id={} in imdb'.format(imdbID))
            my_movie = None
        else:
            my_movie = Movie(imdbID)
            for key in RELEVANT_KEYS:
                setattr(my_movie, key, imdb_movie.data.get(key))
            setattr(my_movie, 'keywords', ia.get_movie_keywords(imdbID)['data'].get('keywords'))
            if my_movie.plot:
                my_movie.plot = [text.split('::')[0] for text in my_movie.plot]
                # alternative to argmin builtin function
                summary_lengths = [len(x) for x in my_movie.plot] 
                f = lambda i: summary_lengths[i]
                smaller = min(range(len(summary_lengths)), key=f)
                my_movie.tagline = my_movie.plot[smaller]
        return my_movie

    def load_best_similar_data(self, collection):
        try:
            results = get_movie_data(collection, self)
        except Exception as e:
            logging.exception(e)
            logging.warning("Failed retrieving best similar data for the movie")
            results = {}
        self.best_similar_themes = results.get('best_similar_themes')
        self.best_similar_recos = results.get('best_similar_recos')

    def load_movie_lens_data(self, movie_lens_api: MovieLensApi, collection):
        try:
            results = movie_lens_api.run(self.title, collection)
        except Exception:
            logging.warning("Failed retrieving movielens for the movie")
            results = {}
        self.movie_lens_recos = results.get("movie_lens_recos")

    @staticmethod
    def load_from_imdb_id(imdbID: str, movie_lens_api: MovieLensApi) -> 'Movie':
        my_movie = Movie._load_imdb_data(imdbID)
        my_movie.load_best_similar_data()
        my_movie.load_movie_lens_data(movie_lens_api)
        return my_movie
    

    @staticmethod
    def load_from_mongodb(imdbID: str, collection) -> 'Movie': 
        mongo_movie = collection.find_one({'imdbID': imdbID})
        if not mongo_movie:
            logging.warning('no movie with id={} in mongo DB'.format(imdbID))
            my_movie = None
        else:
            my_movie = Movie(imdbID)
            for key in vars(my_movie):
                setattr(my_movie, key, mongo_movie.get(key))
        return my_movie


def enrich_and_upload_to_mongo(imdbIDs: list, collection):
    logging.info("connected to mongo DB")
    mv_api = MovieLensApi("mfettaya@hotmail.com", 'raphiphi')
    for imdbID in imdbIDs:
        my_movie = Movie.load_from_imdb_id(imdbID, mv_api)
        my_movie.upload_to_mongo(collection)
    return 0

