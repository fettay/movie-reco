import re
import spacy
import pickle
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

spacy_categories = ['PERSON', 'DATE']
ps = PorterStemmer()
nlp = spacy.load('en_core_web_sm')

class TfIdf:

    def __init__(self, tfidf_path):
        # Need to update code in case there is no pk files and training has to be done from scratch
        self.NNeighbors = pickle.load(open(tfidf_path + "NNeighbors.pk", "rb"))
        self.vectorizer = pickle.load(open(tfidf_path + "vectorizer.pk", "rb"))
        self.mapping = pickle.load(open(tfidf_path + "mapping.pk", "rb"))

    def kneighbors(self, text: str, n:int = 10):
        input_text = TfIdf.text_preprocessing(text)
        vector = self.vectorizer.transform([input_text])
        neighbors = self.NNeighbors.kneighbors(vector, return_distance=False)[0][:n]
        return [self.mapping[neigh] for neigh in neighbors]


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