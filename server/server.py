from flask import Flask
import sys
import pandas as pd
from ml.sentence_recommander import SimilarityRecommander
from ml.themes import ThemeRecommander
from ml.tfidf import TfIdf
from data_management.mongo_utils import movie_from_title, most_popular_titles, get_matching_titles
from flask import jsonify, request
from flask_cors import CORS
from os.path import expanduser


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
    titles = most_popular_titles()
    return jsonify({'results': titles})


@app.route('/autocomplete/<string:text>')
def get_completion(text):
    titles = get_matching_titles(text) if len(text) >= 3 else most_popular_titles()
    return jsonify({'results': titles})


def format_movies(movies):
    return  [{'title': movie.get("title", ""), 
              'genres': movie.get("genres", []),
              'votes': movie.get("votes", 0), 
              'year': movie.get("year", 0)}
              for movie in movies]


@app.route('/movie/<string:recommander_name>/<string:movie>')
def get_movie_reco(recommander_name, movie):
    movies = recommanders[recommander_name].query_movie(movie, 500)
    current_movie = movie_from_title(movie)
    return jsonify({'results': format_movies(movies), 
                    'summary': current_movie.plot[0],
                    'tags': current_movie.best_similar_themes})


@app.route('/ip/<string:recommander_name>', methods=['POST'])
def get_ip_reco(recommander_name):
    ip = request.json.get("ip")
    movies = recommanders[recommander_name].recommand_from_ip(ip, 500)
    return jsonify({'results': format_movies(movies)})


@app.route('/themes', methods=['POST'])
def get_themes_reco():
    ip = request.json.get("ip")
    themes = themes_recommander.get_themes(ip)
    return jsonify({'results': themes})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1994)
    print("Running")
