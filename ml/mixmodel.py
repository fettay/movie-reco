from numpy import array, argsort
from ml.mlmodel import ComparableModel
from ml.tfidf import TfIdf
from ml.theme_algo import RfModel
from data_management.mongo_utils import movies_from_ids, movie_from_title


class MixModel(ComparableModel):
    def __init__(self, tfidf: TfIdf, rfmodel: RfModel):
        self.tfidf = tfidf
        self.theme_model = rfmodel


    def load(self, dirname: str):
        pass


    def order_movies_by_iou(self, ip, ids):
        ip_themes = self.predict_themes(ip)
        my_movies = movies_from_ids(ids)
        if len(ip_themes) == 0:
            return my_movies
        iou_scores = array([MixModel.IoU(ip_themes, m['predicted_themes']) for m in my_movies])
        new_order = argsort(-iou_scores)
        return my_movies[new_order]


    def recommand_from_ip(self, ip: str, n_reco: int=25):
        recommender_ids = self.tfidf._recommand_to_ids(ip)
        recommender_movies = self.order_movies_by_iou(ip, recommender_ids)
        return recommender_movies


    def predict_themes(self, ip: str):
        return self.theme_model.predict_probas_from_ip(ip)


    @staticmethod
    def IoU(themes1, themes2):
        s1, s2 = set(themes1), set(themes2)
        return len(s1&s2) / len(s1|s2)


    def query_movie(self, movie_str: str, n_reco: int=25):
        movie = movie_from_title(movie_str)

        if not hasattr(movie, 'plot'):
            return None
        
        ip = movie.plot

        if ip is None or len(ip) == 0:
            return None
        
        return self.recommand_from_ip(ip[0], n_reco)