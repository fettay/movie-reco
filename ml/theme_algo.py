import pickle
from os import listdir
from ml.mlmodel import ComparableModel
from ml.tfidf import TfIdf, my_tokenizer
from data_management.mongo_utils import movies_from_ids, movie_from_title
from tqdm import tqdm

class RfModel(ComparableModel):

    def __init__(self):
        #logging.basicConfig(level=logging.INFO, filename='/home/israel/logs/theme_algo.log')
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
        theme_probas = self.predict_probas_from_ip(ip)
        neighbors = self.NNeighbors.kneighbors([theme_probas], return_distance=False)[0][:n_reco]
        mapped_ids = [self.mapping[neigh] for neigh in neighbors]
        return mapped_ids


    def recommand_from_ip(self, ip: str, n_reco: int=25):
        ids = self._recommand_to_ids(ip, n_reco)
        return movies_from_ids(ids)


    def predict_themes(self, ip: str):
        theme_probas = self.predict_probas_from_ip(ip)
        theme_predictions = [int(p>0.5) for p in theme_probas]
        theme_predictions = [theme for (i, theme) in zip(range(len(self.trees)), self.trees) \
            if theme_predictions[i]==1]
        return theme_predictions


    def recommand_from_movie(self, movie_name: str, n_reco: int):
        raise NotImplementedError
        

    def predict_probas_from_ip(self, ip: str):
        input_text = TfIdf.text_preprocessing(ip)
        my_vector = self.vectorizer.transform([input_text])
        my_vector = self.scaler.transform(my_vector)
        my_predictions = [self.trees[theme].predict_proba(my_vector)[0][1] for theme in self.trees]
        return my_predictions



