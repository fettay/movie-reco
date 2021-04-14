import logging
import os
from imdb import IMDb
from pymongo import MongoClient


DB_URL = "mongo.fettay.com"
DB_NAME = 'recommander'
DB_COLLECTION = 'movies'


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


    def load_from_imdb(self):
        ia = IMDb()
        imdb_movie = ia.get_movie(self.imdbID)
        if len(imdb_movie) == 0:
            logging.warning('no movie with id={} in imdb'.format(self.imdbID))
        else:
            for key in vars(self):
                setattr(self, key, imdb_movie.data.get(key))
            setattr(self, 'keywords', ia.get_movie_keywords(self.imdbID)['data'].get('keywords'))
            if len(self.plot) > 0:
                # alternative to argmin builtin function
                summary_lengths = [len(x) for x in self.plot] 
                f = lambda i: summary_lengths[i]
                smaller = min(range(len(summary_lengths)), key=f)
                self.tagline = self.plot[smaller] 

    
    def load_from_mongodb(self):
        client = MongoClient("mongodb://{user}:{password}@{url}/".format(user=os.environ['MONGODB_USER'], \
            password=os.environ['MONGODB_PASSWORD'], url=DB_URL))
        db = client[DB_NAME][DB_COLLECTION]    
        mongo_movie = db.find_one({'imdbID': self.imdbID})
        if not mongo_movie:
            logging.warning('no movie with id={} in mongo DB'.format(self.imdbID))
        else:
            for key in vars(self):
                setattr(self, key, mongo_movie.get(key))


my_movie = Movie('0054013')
my_movie.load_from_imdb()
temp = vars(my_movie)
for item in temp:
    print(item, ':', temp[item])
print("\n\n") 
my_movie.load_from_mongodb()
for item in temp:
    print(item, ':', temp[item])

