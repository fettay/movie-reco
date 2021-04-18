def get_connection_url(user, password, url):
    return "mongodb://{user}:{password}@{url}/".format(user=user, password=password, url=url)