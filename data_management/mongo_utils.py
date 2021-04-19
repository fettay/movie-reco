import os

from pymongo import MongoClient

from data_management.constants import DB_URL, DB_NAME, DB_COLLECTION


def get_collection():
    client = MongoClient(get_connection_url(os.environ['MONGODB_USER'], \
                                            os.environ['MONGODB_PASSWORD'], DB_URL))
    return client[DB_NAME][DB_COLLECTION]


def get_connection_url(user, password, url):
    return "mongodb://{user}:{password}@{url}/".format(user=user, password=password, url=url)