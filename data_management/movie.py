import logging
import os
from imdb import IMDb
from pymongo import MongoClient
from multiprocessing import Pool
from constants import DB_URL, DB_NAME, DB_COLLECTION
from mongo_utils import get_connection_url


class Movie:
    def __init__(self, imdbID: str, title: str = '', votes: int = -1, genres: list = [], \
        plot: list = [], synopsis: str = '', keywords: list = [], tagline: str = ''):
        self.imdbID = imdbID
        self.title = title
        self.votes = votes
        self.genres = genres
        self.plot = plot
        self.synopsis = synopsis
        self.keywords = keywords
        self.tagline = tagline


    def upload_to_mongo(self, db_connection, overwrite=True):
        db_connection.update_one({'imdbID': self.imdbID}, {'$set': vars(self)}, overwrite)
        logging.info("id movie {} saved to mongo DB".format(self.imdbID))
        return 0


    @staticmethod
    def load_from_imdb(imdbID: str) -> 'Movie':
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
    

    @staticmethod
    def load_from_mongodb(imdbID: str) -> 'Movie':
        client = MongoClient("mongodb://{user}:{password}@{url}/".format(user=os.environ['MONGODB_USER'], \
            password=os.environ['MONGODB_PASSWORD'], url=DB_URL))
        db = client[DB_NAME][DB_COLLECTION]    
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
    client = MongoClient(get_connection_url(os.environ['MONGODB_USER'], \
                                            os.environ['MONGODB_PASSWORD'], "mongo.fettay.com"))
    db = client[DB_NAME][DB_COLLECTION]
    logging.info("connected to mongo DB")
    for imdbID in imdbIDs:
        my_movie = Movie.load_from_imdb(imdbID)
        my_movie.upload_to_mongo(db)
    return 0

