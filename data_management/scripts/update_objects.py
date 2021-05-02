from tqdm.contrib.concurrent import process_map
from tqdm import tqdm
# import sys
# sys.path.insert(0, '/home/israel/movie-reco')
from data_management.mongo_utils import get_collection
from data_management.movie import Movie


def _add_best_similar_data(id_):
    collection = get_collection()
    m = collection.find_one({"_id": id_})
    m = Movie(**m)
    m.load_best_similar_data()
    m.upload_to_mongo(collection)
    

def add_best_similar_data():
    collection = get_collection()
    ids = collection.find().distinct('_id')
    process_map(_add_best_similar_data, ids, max_workers=10, chunksize=100)


def add_imdb_data(fields):
    collection = get_collection()
    imdb_ids = collection.find({'imdbID': {'$ne': None}}).distinct('imdbID')
    print(len(imdb_ids), " movies to update")
    for i, imdbID in tqdm(enumerate(imdb_ids[::-1]), total=len(imdb_ids)):
        m = Movie(imdbID)
        m.enrich_from_imdb(fields)


if __name__ == "__main__":
    # add_imdb_data(['year'])

