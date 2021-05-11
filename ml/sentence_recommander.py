import numpy as np
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
import numpy as np
import spacy
import regex as re
import pickle

from data_management.mongo_utils import movies_from_ids, movie_from_title
from ml.mlmodel import ComparableModel


class SimilarityRecommander(ComparableModel):
    
    def __init__(self, field):
        self.embeddings = None
        self.sentence_transformer = None
        self.nlp = None
        self.field = field
    
    def load(self, dirname, embedding=True):
        if embedding:
            with open(dirname + "/embeddings.pkl", "rb") as f:
                self.embeddings = pickle.load(f)
        self.sentence_transformer = SentenceTransformer(dirname + "/transformer/")
        self.nlp = spacy.load("en_core_web_sm")
        return self
        
    def _get_reco_from_embedding(self, embedding):
        distances = np.array([cosine(e, embedding) for e in self.embeddings.values()])
        keys = np.array(list(self.embeddings.keys()))
        best_indexes = distances.argsort()
        movies_sorted = movies_from_ids(keys[best_indexes].tolist())
        return movies_sorted

    def _replace_ents(self, sentence):
        sentence = re.sub("[\(\[].*?[\)\]]", "", sentence)  # Drop content in parenthesis
        replace_token = ""
        ents = self.nlp(sentence).ents
        dropped_vals = 0
        dropped_ents = set()
        for ent in ents:
            if ent.label_ in ["PERSON", "ORG", "WORK_OF_ART", "TIME", "FAC"]:
                sentence = sentence[:ent.start_char - dropped_vals] + replace_token  + sentence[ent.end_char - dropped_vals:]
                dropped_vals += (ent.end_char - ent.start_char - len(replace_token))
                dropped_ents.add(str(ent))
        
        # Doing another pass to make sure we didn't forget some
        dropped_ents = sorted(list(dropped_ents), key=lambda x: -len(x))
        for ent in dropped_ents:
            sentence = sentence.replace(ent, replace_token)
        return sentence
        
    def query_movie(self, movie_str: str, n_reco: int=25):
        movie = movie_from_title(movie_str)

        if not hasattr(movie, self.field):
            return None

        ip = getattr(movie, self.field)

        if ip is None or len(ip) == 0:
            return None
        
        return self.recommand_from_ip(ip[0], n_reco)
    
    def recommand_from_ip(self, ip: str, n_reco: int=25):
        ip = self._replace_ents(ip)
        new_embedding = self.sentence_transformer.encode([ip], show_progress_bar=False)
        movies_sorted = self._get_reco_from_embedding(new_embedding)
        return movies_sorted[1:n_reco + 1]