from flask import Flask
import sys
import pandas as pd
from os.path import expanduser
sys.path.insert(0, expanduser("~/movie-reco/"))
from ml.sentence_recommander import SimilarityRecommander
from ml.themes import ThemeRecommander
from ml.tfidf import TfIdf, my_tokenizer
from ml.theme_algo import RfModel
from ml.mixmodel import MixModel
from ml.theme_lgbm import ThemePredictor
from data_management.mongo_utils import movie_from_title, most_popular_titles, get_matching_titles
from flask import jsonify, request
from flask_cors import CORS


app = Flask(__name__)
MODELS_PATH = expanduser("~") + "/research/models/"
THEME_THRLD = 0.5

THEMES_DATA = {'tokenizer_path': "distilbert-base-uncased",
               "model_path": "models/themes"}
CORS(app)

recommanders = {'TfIdf': TfIdf().load(MODELS_PATH + "tfidf/"),
                'TreeDecision': ThemePredictor().load(MODELS_PATH + "theme_lgbm/")}
recommanders['Mix'] = MixModel(recommanders['TfIdf'], recommanders['TreeDecision'])


@app.route('/autocomplete/', defaults={'text': None})
@app.route('/autocomplete/<string:text>')
def get_completion(text):
    if text:
        titles = get_matching_titles(text)
    else:
        titles = most_popular_titles()
    return jsonify({'results': titles})


def format_movies(movies):
    return  [{'title': movie.get("title", ""), 
              'genres': movie.get("genres", []),
              'votes': movie.get("votes", 0), 
              'year': movie.get("year", 0),
              'cover_url': movie.get("cover_url", ""),
              'tagline': movie.get("tagline", ""),
              'id': movie.get("imdbID"),
              'themes': movie.get('predicted_themes', [])}  
              for movie in movies]


@app.route('/movie/<string:recommander_name>/<string:movie>')
def get_movie_reco(recommander_name, movie):
    movies = recommanders[recommander_name].recommand_from_movie(movie, 500)
    ip = movie_from_title(movie).get('plot_outline', '')
    return jsonify({'results': format_movies(movies),
                    'movie_ip': ip})


@app.route('/ip/<string:recommander_name>', methods=['POST'])
def get_ip_reco(recommander_name):
    ip = request.json.get("ip")
    movies = recommanders[recommander_name].recommand_from_ip(ip, 500)
    themes = recommanders['TreeDecision'].predict_themes(ip, THEME_THRLD)
    return jsonify({'results': format_movies(movies),
                    'themes': themes})


@app.route('/themes', methods=['POST'])
def get_themes_reco(recommander_name):
    ip = request.json.get("ip")
    themes = recommanders[recommander_name].predict_themes(ip, THEME_THRLD)
    return jsonify({'results': themes})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1994)
    print("Running")
