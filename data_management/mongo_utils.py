import os

import re

from pymongo import MongoClient, collection

from data_management.constants import DB_URL, DB_NAME, DB_COLLECTION, N_AUTOCOMPLETE
from data_management.movie import Movie


def get_collection():
    client = MongoClient(get_connection_url(os.environ['MONGODB_USER'], \
                                            os.environ['MONGODB_PASSWORD'], DB_URL))
    return client[DB_NAME][DB_COLLECTION]


def get_connection_url(user, password, url):
    return "mongodb://{user}:{password}@{url}/".format(user=user, password=password, url=url)


def movies_from_ids(object_ids):
    collection = get_collection()
    return [Movie(**list(collection.find({"_id": object_id}))[0]) for object_id in object_ids]


def movie_from_title(title: str):
    collection = get_collection()
    result = collection.find_one({"title": title})
    return Movie(**result)


def get_all_movies_title():
    collection = get_collection()
    return list(collection.find().distinct('title'))


def most_popular_titles():
    collection = get_collection()
    query = list(collection.find({}, {"title": 1, "_id": 0}).sort([("votes", -1)]).limit(N_AUTOCOMPLETE))
    titles = [q['title'] for q in query]
    return titles


def get_matching_titles(text: str):
    collection = get_collection()
    regex = "(^| )(?i)" + text
    query = list(collection.find({"title": {"$regex": regex}}, {"_id": 0, "title": 1}))
    titles = [q['title'] for q in query][:N_AUTOCOMPLETE]
    return titles