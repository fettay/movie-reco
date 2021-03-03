import numpy as np
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
import numpy as np
import spacy
import regex as re


class SimilarityRecommander():
    
    def __init__(self, dataset, field, embeddings=None, sentence_transformer=None, min_votes=300):
        self.df = dataset[dataset['vote_count'] > min_votes].copy().reset_index(drop=True)
        self.movies_map = {row['title']: i for i, row in self.df.iterrows()}
        self.embeddings = embeddings
        self.sentence_transformer = sentence_transformer
        self.nlp = spacy.load("en_core_web_sm")
        self.field = field
    
    @staticmethod
    def _jaccard_similarity(list1, list2):
        intersection = len(set(list1).intersection(list2))
        union = (len(list1) + len(list2)) - intersection
        return float(intersection) / union
    
    def compute_jaccards(self, index):
        current_genres = self.df.loc[index]['genres'].split("|")
        all_genres = [row['genres'].split("|") for _, row in self.df.iterrows()]
        return [SimilarityRecommander._jaccard_similarity(current_genres, g) for g in all_genres]
        
    def train(self):
        self.embeddings = self.sentence_transformer.encode(self.df[self.field].astype(str).tolist(),
                                                           show_progress_bar=False)
        
    def _get_reco_from_embedding(self, embedding, mask=None):
        distances = np.array([cosine(e, embedding) for e in self.embeddings])
        best_indexes = distances.argsort()
        if mask is not None:
            best_indexes = [ind for ind in best_indexes if mask[ind]]
        movies_sorted = [self.df.loc[i]['title'] for i in best_indexes]
        return distances, movies_sorted

    def replace_ents(self, sentence):
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

    def get_summary(self, movie_str):
        index = self.movies_map[movie_str]
        return self.df.loc[index][self.field.replace("_clean", "")]

    def get_tags(self, movie_str):
        index = self.movies_map[movie_str]
        tags = self.df.loc[index]['tags']
        tags = tags.split("|")
        tags = [t for t in tags if not t[0].isupper()]
        return tags
        
    def query_movie(self, movie_str):
        index = self.movies_map[movie_str]
#         jaccards_mask = [s > .5 for s in self.compute_jaccards(index)]
        embed = self.embeddings[index]
        _, movies_sorted = self._get_reco_from_embedding(embed, mask=None)
        return movies_sorted[1:25]
    
    def from_ip(self, ip):
        ip = self.replace_ents(ip)
        new_embedding = self.sentence_transformer.encode(ip, show_progress_bar=False)
        distances, movies_sorted = self._get_reco_from_embedding(new_embedding)
        print(distances)
        return movies_sorted[1:25]