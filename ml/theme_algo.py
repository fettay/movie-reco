import pickle
from os import listdir
from ml.mlmodel import ComparableModel
from ml.tfidf import TfIdf, my_tokenizer
from data_management.mongo_utils import movies_from_ids, movie_from_title
from tqdm import tqdm

class RfModel(ComparableModel):

    def __init__(self):
        pass


    def load(self, dirname: str):
        self.NNeighbors = pickle.load(open(dirname + "NNeighbors.pk", "rb"))
        self.mapping = pickle.load(open(dirname + "mapping.pk", "rb"))
        self.scaler = pickle.load(open(dirname + "scaler.pk", "rb"))
        self.vectorizer = pickle.load(open(dirname + "vectorizer.pk", "rb"))
        self.tree_directory = dirname + "trees/"
        all_themes = listdir(self.tree_directory)
        self.trees = {theme.split('.pk')[0]: pickle.load(open(self.tree_directory+theme, "rb")) \
                                for theme in tqdm(all_themes)}
        return self


    def _recommand_to_ids(self, ip: str, n_reco: int):
        # input_text = TfIdf.text_preprocessing(ip)
        # my_vector = self.vectorizer.transform([input_text])
        # my_vector = self.scaler.transform(my_vector)
        theme_predictions = self.predict_themes_from_ip(ip)
        neighbors = self.NNeighbors.kneighbors([theme_predictions], return_distance=False)[0][:n_reco]
        return [self.mapping[neigh] for neigh in neighbors]


    def recommand_from_ip(self, ip: str, n_reco: int=25):
        ids = self._recommand_to_ids(ip, n_reco)
        return [movies_from_ids([_id])[0] for _id in ids]


    def recommand_from_movie(self, movie_name: str, n_reco: int):
        raise NotImplementedError
        

    def predict_themes_from_ip(self, ip: str):
        input_text = TfIdf.text_preprocessing(ip)
        my_vector = self.vectorizer.transform([input_text])
        my_vector = self.scaler.transform(my_vector)
        #theme_predictions = [model.predict_proba(my_vector)[0][1] for model in self.trees.values()]
        return [self.trees[theme].predict(my_vector)[0] for theme in self.trees]


    def query_movie(self, movie_str: str, n_reco: int=25):
        movie = movie_from_title(movie_str)

        if not hasattr(movie, 'plot'):
            return None
        
        ip = movie.plot

        if ip is None or len(ip) == 0:
            return None
        
        return self.recommand_from_ip(ip[0], n_reco)


