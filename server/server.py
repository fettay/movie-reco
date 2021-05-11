from flask import Flask
import pandas as pd
from ml.sentence_recommander import SimilarityRecommander
from ml.themes import ThemeRecommander
from ml.tfidf import TfIdf
from data_management.mongo_utils import movie_from_title
from flask import jsonify, request
from flask_cors import CORS
import os
from os.path import expanduser
import pickle


app = Flask(__name__)
MODELS_PATH = expanduser("~") + "/research/models/"

THEMES_DATA = {'tokenizer_path': "distilbert-base-uncased",
               "model_path": "models/themes"}
CORS(app)

recommanders = {'tagline' : SimilarityRecommander("tagline").load(MODELS_PATH + "tagline"),
                'storyline': TfIdf().load(MODELS_PATH + "tfidf"),
                'synopsis': SimilarityRecommander("synopsis").load(MODELS_PATH + "synopsis")}

themes_recommander = ThemeRecommander(**THEMES_DATA)

@app.route('/autocomplete')
def get_completion_all():
    return jsonify({'results': []})


@app.route('/autocomplete/<string:text>')
def get_completion(text):
    # text = text.lower()
    # match = [m for m in recommanders[DEFAULT_RECOMMANDER].movies_map if text in m.lower()]
    # match = match[:50]
    return jsonify({'results': []})


@app.route('/movie/<string:recommander_name>/<string:movie>')
def get_movie_reco(recommander_name, movie):
    movies = recommanders[recommander_name].query_movie(movie)
    current_movie = movie_from_title(movie)
    return jsonify({'results': [m.title for m in movies], 
                    'summary': current_movie.plot[0],
                    'tags': current_movie.best_similar_themes})


@app.route('/ip/<string:recommander_name>', methods=['POST'])
def get_ip_reco(recommander_name):
    ip = request.json.get("ip")
    movies = recommanders[recommander_name].recommand_from_ip(ip)
    return jsonify({'results': [movie.title for movie in movies]})


@app.route('/themes', methods=['POST'])
def get_themes_reco():
    ip = request.json.get("ip")
    themes = themes_recommander.get_themes(ip)
    return jsonify({'results': themes})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1994)
    print("Running")