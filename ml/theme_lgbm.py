import pickle
from os import listdir
from ml.tfidf import TfIdf, my_tokenizer
from data_management.mongo_utils import movies_from_ids, movie_from_title
from tqdm import tqdm

class ThemePredictor:

    def __init__(self):
        #logging.basicConfig(level=logging.INFO, filename='/home/israel/logs/theme_algo.log')
        pass


    def load(self, dirname: str):
        self.scaler = pickle.load(open(dirname + "scaler.pk", "rb"))
        self.vectorizer = pickle.load(open(dirname + "vectorizer.pk", "rb"))
        self.tree_directory = dirname + "trees/"
        all_themes = listdir(self.tree_directory)
        self.trees = {theme.split('.pk')[0]: pickle.load(open(self.tree_directory+theme, "rb")) \
                                for theme in tqdm(all_themes)}
        return self


    def predict_themes(self, ip: str, thd=0.5):
        theme_probas = self.predict_probas(ip)
        theme_predictions = [int(p>thd) for p in theme_probas]
        theme_predictions = [theme for (i, theme) in zip(range(len(self.trees)), self.trees) \
            if theme_predictions[i]==1]
        return theme_predictions


    def predict_themes_from_movie(self, movie_name: str, thd=0.5):
        my_movie = movie_from_title(movie_name)
        ip = my_movie.get('plot_outline', '')
        return self.predict_themes(ip, thd)


    def predict_probas(self, ip: str):
        input_text = TfIdf.text_preprocessing(ip)
        my_vector = self.vectorizer.transform([input_text])
        my_vector = self.scaler.transform(my_vector)
        my_predictions = [self.trees[theme].predict(my_vector)[0] for theme in self.trees]
        return my_predictions