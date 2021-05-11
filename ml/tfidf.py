import re
import spacy
import pickle
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from ml.mlmodel import ComparableModel
from data_management.mongo_utils import movies_from_ids, movie_from_title


spacy_categories = ['PERSON', 'DATE']
ps = PorterStemmer()
nlp = spacy.load('en_core_web_sm')

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
        return 

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
        text = text.replace("_", "")
        for ent in nlp(text).ents:
            if ent.label_ in spacy_categories:
                filters = ent.text.split()
                for fil in filters:
                    text = text.replace(fil, "")
        text = text.lower()
        words = re.findall('[a-zA-Z]{2,}', text)
        words = [w for w in words if w not in stopwords.words('english')]
        words = [ps.stem(w) for w in words]
        return ' '.join(words)