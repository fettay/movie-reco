from typing import List
import logging
import os

from imdb import IMDb
from bson.objectid import ObjectId

from data_management.mongo_utils import get_collection
from data_management.utils.best_similar import get_movie_data


class Movie:
    def __init__(self, imdbID: str, title: str = '', votes: int = -1, genres: list = [], \
        plot: list = [], synopsis: str = '', keywords: list = [], tagline: str = '',
        best_similar_themes: List[str] = None, best_similar_recos: List[ObjectId] = None,
        **kwargs):
        self.imdbID = imdbID
        self.title = title
        self.votes = votes
        self.genres = genres
        self.plot = plot
        self.synopsis = synopsis
        self.keywords = keywords
        self.tagline = tagline
        self.best_similar_themes = best_similar_themes
        self.best_similar_recos = best_similar_recos


    def upload_to_mongo(self, db_connection, overwrite=True):
        db_connection.update_one({'imdbID': self.imdbID}, {'$set': vars(self)}, overwrite)
        logging.info("id movie {} saved to mongo DB".format(self.imdbID))
        return 0

    @staticmethod
    def _load_imdb_data(imdbID: str) -> 'Movie':
        ia = IMDb()
        imdb_movie = ia.get_movie(imdbID)
        if len(imdb_movie) == 0:
            logging.warning('no movie with id={} in imdb'.format(imdbID))
            my_movie = None
        else:
            my_movie = Movie(imdbID)
            for key in vars(my_movie):
                setattr(my_movie, key, imdb_movie.data.get(key))
            setattr(my_movie, 'keywords', ia.get_movie_keywords(imdbID)['data'].get('keywords'))
            if my_movie.plot:
                # alternative to argmin builtin function
                summary_lengths = [len(x) for x in my_movie.plot] 
                f = lambda i: summary_lengths[i]
                smaller = min(range(len(summary_lengths)), key=f)
                my_movie.tagline = my_movie.plot[smaller]
        return my_movie

    def load_best_similar_data(self):
        collection = get_collection()
        results = get_movie_data(collection, self)
        self.best_similar_themes = results.get('best_similar_themes')
        self.best_similar_recos = results.get('best_similar_recos')

    @staticmethod
    def load_from_imdb_id(imdbID: str) -> 'Movie':
        my_movie = Movie._load_imdb_data(imdbID)
        my_movie.load_best_similar_data()
        return my_movie
    

    @staticmethod
    def load_from_mongodb(imdbID: str) -> 'Movie':
        db = get_collection()  
        mongo_movie = db.find_one({'imdbID': imdbID})
        if not mongo_movie:
            logging.warning('no movie with id={} in mongo DB'.format(imdbID))
            my_movie = None
        else:
            my_movie = Movie(imdbID)
            for key in vars(my_movie):
                setattr(my_movie, key, mongo_movie.get(key))
        return my_movie


def enrich_and_upload_to_mongo(imdbIDs: list):
    db = get_collection()
    logging.info("connected to mongo DB")
    for imdbID in imdbIDs:
        my_movie = Movie.load_from_imdb_id(imdbID)
        my_movie.upload_to_mongo(db)
    return 0

