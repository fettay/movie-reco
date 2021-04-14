import numpy as np
import os
import pandas as pd
import re
import logging
from imdb import IMDb
from multiprocessing import Pool
from pymongo import MongoClient


RELEVANT_KEYS = ['imdbID', 'title', 'genres', 'votes', 'plot', 'synopsis']


def get_connection_url(user, password, url):
    return "mongodb://{user}:{password}@{url}/".format(user=user, password=password, url=url)


def enrich_movie(movie_id, only_english=True):
    ia = IMDb()
    movie = ia.get_movie(movie_id)
    if len(movie) == 0:
        return {}
    if only_english and 'en' not in ia.get_movie(movie_id).data.get('language codes', ''):
        return {}
    mongo_movie = {key: movie.data.get(key) for key in RELEVANT_KEYS}
    mongo_movie["keywords"] = ia.get_movie_keywords(movie.movieID)['data'].get('keywords')
    plots = movie.data.get('plot')
    if plots:
        smaller = np.argmin([len(x) for x in plots])
        mongo_movie['tagline'] = plots[smaller]
    return mongo_movie


def upload_movie_to_mongo(movie_id):
    data = enrich_movie(movie_id)
    if len(data) > 0:
        db.update_one({'imdbID': data['imdbID']}, {'$set': data}, True)
        return movie_id
    return 0


if __name__ == "__main__":
    logging.basicConfig(level='INFO')
    logging.info("SCRIPT IS STARTED")
    client = MongoClient(get_connection_url(os.environ['MONGODB_USER'], \
                                            os.environ['MONGODB_PASSWORD'], "mongo.fettay.com"))
    db = client["recommander"]['movies']
    logging.info("CONNECTED TO MONGO")
    my_df = pd.read_table("/home/fettay/research/titles_imdb.tsv", delimiter='\t')
    my_df = my_df[(my_df.titleType == 'movie') & (my_df.startYear.apply(lambda x: int(x) if x != '\\N' else 0) > 1960)]
    all_ids = [re.findall('[0-9]+', x)[0] for x in my_df.tconst.values]
    all_ids = all_ids[74945:]
    logging.info("{} IDS READY".format(len(all_ids)))
    with Pool(3) as p:
        res = list(p.map(upload_movie_to_mongo, all_ids))
