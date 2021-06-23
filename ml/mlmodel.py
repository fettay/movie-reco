from data_management.mongo_utils import movie_from_title


class ComparableModel:

    def __init__(self):
        pass


    def load(self, dirname: str):
        return


    def recommand_from_ip(self, ip: str, n_reco: int):
        raise NotImplementedError


    def recommand_from_movie(self, movie_name: str, n_reco: int):
        my_movie = movie_from_title(movie_name)
        ip = my_movie.get('plot_outline', '')
        return self.recommand_from_ip(ip, n_reco)


    def predict_themes(self, ip: str):
        return []