class ComparableModel:

    def __init__(self):
        pass

    def load(self, dirname: str):
        return

    def recommand_from_ip(self, ip: str, n_reco: int):
        raise NotImplementedError

    def recommand_from_movie(self, movie_name: str, n_reco: int):
        raise NotImplementedError
