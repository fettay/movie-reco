import logging

from tqdm.contrib.concurrent import process_map
from tqdm import tqdm

from data_management.mongo_utils import get_collection
from data_management.movie import Movie
from data_management.utils.movie_lens import MovieLensApi

def _add_best_similar_data(id_):
    collection = get_collection()
    m = collection.find_one({"_id": id_})
    if not m.get("best_similar_recos") is None:
        return
    m = Movie(**m)
    m.load_best_similar_data()
    m.upload_to_mongo(collection)
    if m.best_similar_themes is None:
        logging.info("Updated movie %s but found nothing" % m.title)
    else:
        logging.info("Updated movie %s and found data" % m.title)
    return 
    

def add_best_similar_data():
    collection = get_collection()
    ids = collection.find().distinct('_id')
    process_map(_add_best_similar_data, ids, max_workers=10, chunksize=100)


def add_movie_lens_data():
    collection = get_collection()
    api = MovieLensApi('mfettaya@hotmail.com', "zxczxczxc")
    ids = collection.find().distinct('_id')
    for id_ in tqdm(ids):
        collection = get_collection()
        m = collection.find_one({"_id": id_})
        if "movie_lens_recos" in m:
            continue
        m = Movie(**m)
        m.load_movie_lens_data(api)
        m.upload_to_mongo(collection)


if __name__ == "__main__":
    pass

