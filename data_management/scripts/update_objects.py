from tqdm.contrib.concurrent import process_map
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


if __name__ == "__main__":
    add_best_similar_data()



