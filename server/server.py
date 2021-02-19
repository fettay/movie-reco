from flask import Flask
from sentence_transformers import SentenceTransformer
import pandas as pd
from ml import SimilarityRecommander
from flask import jsonify, request
from sklearn.manifold import TSNE
from flask_cors import CORS
import os
import pickle


app = Flask(__name__)
MODEL_PATH = "models/summary_and_plots"
DATASET_PATH = "models/dataset_new.csv"
CACHE_PATH_EMBEDDINGS = "models/cache/embeddings.pkl"
CACHE_PATH_MAP = "models/cache/maps.pkl"
CORS(app)


dataset = pd.read_csv(DATASET_PATH)
sentence_transformer = SentenceTransformer(MODEL_PATH, device='cpu')
recommander = SimilarityRecommander(dataset, sentence_transformer=sentence_transformer)

if os.path.exists(CACHE_PATH_EMBEDDINGS):
    with open(CACHE_PATH_EMBEDDINGS, "rb") as f:
        recommander.embeddings = pickle.load(f)
else:
    recommander.train()
    with open(CACHE_PATH_EMBEDDINGS, "wb") as f:
        pickle.dump(recommander.embeddings, f)

if os.path.exists(CACHE_PATH_MAP):
    with open(CACHE_PATH_MAP, "rb") as f:
        x, hover = pickle.load(f)
else:
    tsne = TSNE(n_components=2, metric='cosine')
    x = tsne.fit_transform(recommander.embeddings)
    hover = recommander.df['title'].values
    with open(CACHE_PATH_MAP, "wb") as f:
        pickle.dump((x, hover), f)


@app.route('/autocomplete')
def get_completion_all():
    match = [m for m in recommander.movies_map]
    return jsonify({'results': match})


@app.route('/autocomplete/<string:text>')
def get_completion(text):
    text = text.lower()
    match = [m for m in recommander.movies_map if text in m.lower()]
    return jsonify({'results': match})


@app.route('/movie/<string:movie>')
def get_movie_reco(movie):
    movies = recommander.query_movie(movie)
    return jsonify({'results': movies, 'summary': recommander.get_summary(movie)})


@app.route('/ip', methods=['POST'])
def get_ip_reco():
    ip = request.json.get("ip")
    movies = recommander.from_ip(ip)
    return jsonify({'results': movies})


@app.route('/map')
def get_map():
    return jsonify({'x': x[:, 0].tolist(), 'y': x[:, 1].tolist(), 'hover': hover.tolist()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1994)
    print("Running")