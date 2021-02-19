import numpy as np
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
import numpy as np
import spacy


class SimilarityRecommander():
    
    def __init__(self, dataset, embeddings=None, sentence_transformer=None, min_votes=300):
        self.df = dataset[dataset['vote_count'] > min_votes].copy().reset_index(drop=True)
        self.movies_map = {row['title']: i for i, row in self.df.iterrows()}
        self.embeddings = embeddings
        self.sentence_transformer = sentence_transformer
        self.nlp = spacy.load("en_core_web_sm")
    
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
        self.embeddings = self.sentence_transformer.encode(self.df['summary'].astype(str).tolist(),
                                                           show_progress_bar=False)
        
    def _get_reco_from_embedding(self, embedding, mask=None):
        distances = np.array([cosine(e, embedding) for e in self.embeddings])
        best_indexes = distances.argsort()
        if mask is not None:
            best_indexes = [ind for ind in best_indexes if mask[ind]]
        movies_sorted = [self.df.loc[i]['title'] for i in best_indexes]
        return distances, movies_sorted

    def replace_ents(self, sentence):
        ents = self.nlp(sentence).ents
        for ent in set(ents):
            sentence = sentence.replace(str(ent), "<ukn>")
        return sentence

    def get_summary(self, movie_str):
        index = self.movies_map[movie_str]
        return self.df.loc[index]['summary']
        
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