import os

from pymongo import MongoClient

from data_management.constants import DB_URL, DB_NAME, DB_COLLECTION
from data_management.movie import Movie


def get_collection():
    client = MongoClient(get_connection_url(os.environ['MONGODB_USER'], \
                                            os.environ['MONGODB_PASSWORD'], DB_URL))
    return client[DB_NAME][DB_COLLECTION]


def get_connection_url(user, password, url):
    return "mongodb://{user}:{password}@{url}/".format(user=user, password=password, url=url)


def movies_from_ids(object_ids):
    collection = get_collection()
    return [Movie(**kwargs) for kwargs in list(collection.find({"_id": {"$in": object_ids}}))]


def movie_from_title(title: str):
    collection = get_collection()
    result = collection.find_one({"title": title})
    return Movie(**result)


def get_all_movies_title():
    collection = get_collection()
    return list(collection.find().distinct('title'))
