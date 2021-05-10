from flask import Flask
from sentence_transformers import SentenceTransformer
import pandas as pd
from ml.sentence_recommander import SimilarityRecommander
from ml.themes import ThemeRecommander
from ml.tfidf import TfIdf
from flask import jsonify, request
from sklearn.manifold import TSNE
from flask_cors import CORS
import os
import pickle


app = Flask(__name__)
MODEL_PATH = {'tagline': "distilbert-base-nli-stsb-mean-tokens", 'storyline': "distilbert-base-nli-stsb-mean-tokens", "synopsis": "models/synopsis"}
DATASET_PATH = "models/dataset_new.csv"
CACHE_DIR = "models/cache/"
CACHE_PATH_EMBEDDINGS = CACHE_DIR + "embeddings.pkl"
CACHE_PATH_MAP = CACHE_DIR + "maps.pkl"
DEFAULT_RECOMMANDER = "storyline"
TF_IDF_PATH = "models/tfidf/"

THEMES_DATA = {'tokenizer_path': "distilbert-base-uncased",
               "model_path": "models/themes"}
CORS(app)

dataset = pd.read_csv(DATASET_PATH)
recommanders = {'tagline' : SimilarityRecommander(dataset, "tagline_clean",
                            sentence_transformer=SentenceTransformer(MODEL_PATH['tagline'], device='cpu')),
                'storyline': SimilarityRecommander(dataset, "plot_summary_clean",
                 sentence_transformer=SentenceTransformer(MODEL_PATH['storyline'], device='cpu')),
                'synopsis': SimilarityRecommander(dataset, "synopsis_clean",
                 sentence_transformer=SentenceTransformer(MODEL_PATH['synopsis'], device='cpu'))}

themes_recommander = ThemeRecommander(**THEMES_DATA)

# if not os.path.exists(CACHE_DIR):
#     os.makedirs(CACHE_DIR)

# if os.path.exists(CACHE_PATH_EMBEDDINGS):
#     with open(CACHE_PATH_EMBEDDINGS, "rb") as f:
#         all_embeddings = pickle.load(f)
#         for k in recommanders:
#             recommanders[k].embeddings = all_embeddings[k]
# else:
#     for k in recommanders:
#         recommanders[k].train()
#     with open(CACHE_PATH_EMBEDDINGS, "wb") as f:
#         pickle.dump({k: recommanders[k].embeddings for k in recommanders}, f)

# if os.path.exists(CACHE_PATH_MAP):
#     with open(CACHE_PATH_MAP, "rb") as f:
#         x, hover = pickle.load(f)
# else:
#     tsne = TSNE(n_components=2, metric='cosine')
#     x = tsne.fit_transform(recommanders[DEFAULT_RECOMMANDER].embeddings)
#     hover = recommanders[DEFAULT_RECOMMANDER].df['title'].values
#     with open(CACHE_PATH_MAP, "wb") as f:
#         pickle.dump((x, hover), f)


@app.route('/autocomplete')
def get_completion_all():
    match = [m for m in recommanders[DEFAULT_RECOMMANDER].movies_map]
    match = match[:50]
    return jsonify({'results': match})


@app.route('/autocomplete/<string:text>')
def get_completion(text):
    text = text.lower()
    match = [m for m in recommanders[DEFAULT_RECOMMANDER].movies_map if text in m.lower()]
    match = match[:50]
    return jsonify({'results': match})


@app.route('/movie/<string:recommander_name>/<string:movie>')
def get_movie_reco(recommander_name, movie):
    movies = recommanders[recommander_name].query_movie(movie)
    return jsonify({'results': movies, 'summary': recommanders[recommander_name].get_summary(movie),
                    'tags': recommanders[recommander_name].get_tags(movie)})


@app.route('/ip/<string:recommander_name>', methods=['POST'])
def get_ip_reco(recommander_name):
    ip = request.json.get("ip")
    movies = recommanders[recommander_name].from_ip(ip)
    return jsonify({'results': movies})


@app.route('/themes', methods=['POST'])
def get_themes_reco():
    ip = request.json.get("ip")
    themes = themes_recommander.get_themes(ip)
    return jsonify({'results': themes})


@app.route('/map')
def get_map():
    return jsonify({'x': x[:, 0].tolist(), 'y': x[:, 1].tolist(), 'hover': hover.tolist()})


@app.route('/tfidf/<string:text>')
def return_kneighbors(text):
    reco = TfIdf(TF_IDF_PATH)
    match = reco.kneighbors(text)
    return str(match)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1994)
    print("Running")