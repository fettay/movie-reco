import re
import pickle
from nltk import ngrams
from nltk.stem import PorterStemmer

from ml.mlmodel import ComparableModel
from data_management.mongo_utils import movies_from_ids, movie_from_title


ps = PorterStemmer()
stopwords = open("/home/israel/research/models/stopwords.txt", "r").read().split(', ')


class TfIdf(ComparableModel):

    def __init__(self):
        # Need to update code in case there is no pk files and training has to be done from scratch
        self.NNeighbors = None
        self.vectorizer = None
        self.mapping = None
    
    def load(self, dirname: str):
        self.NNeighbors = pickle.load(open(dirname + "/NNeighbors.pk", "rb"))
        self.vectorizer = pickle.load(open(dirname + "/vectorizer.pk", "rb"))
        self.mapping = pickle.load(open(dirname + "/mapping.pk", "rb"))
        return self

    def _recommand_to_ids(self, ip: str, n_reco):
        input_text = TfIdf.text_preprocessing(ip)
        vector = self.vectorizer.transform([input_text])
        neighbors = self.NNeighbors.kneighbors(vector, return_distance=False)[0][:n_reco]
        return [self.mapping[neigh] for neigh in neighbors]
    
    
    def recommand_from_ip(self, ip: str, n_reco: int=25):
        ids = self._recommand_to_ids(ip, n_reco)
        return movies_from_ids(ids)

    def query_movie(self, movie_str: str, n_reco: int=25):
        movie = movie_from_title(movie_str)

        if not hasattr(movie, 'plot'):
            return None
        
        ip = movie.plot

        if ip is None or len(ip) == 0:
            return None
        
        return self.recommand_from_ip(ip[0], n_reco)

    @staticmethod
    def text_preprocessing(text: str) -> str:
        text = text.lower()
        words = re.findall('[a-zA-Z-]{2,}|[,;:\.]', text)
        words = [w.replace('.', ' |').replace(',', ' |').replace(':', '|').replace(';', '|') for w in words]
        words = [w if w not in stopwords else '|' for w in words]
        words = [ps.stem(w) for w in words]
        return ' '.join(words)


def n_gram(text, n):
    return [" ".join(x) for x in list(ngrams(text.split(), n)) if '|' not in x]


def my_tokenizer(text):
    my_tokens = text.split() + n_gram(text, 2) + n_gram(text, 3)
    return [t for t in my_tokens if t!='|']
