from flask import Flask, render_template, request
from joblib import load
import pandas as pd
import json

# pipeline = load('MODEL/model.joblib')


def create_app():
    """Create and configure a basic Flask app"""
    app = Flask(__name__)

    @app.route('/')
    def root():
        return render_template('base.html')

    @app.route('/input', methods=['POST'])
    def retrieval():
        try:
            requestJson = json.loads(request.data)
            liked_songs = requestJson['liked_songs']
            disliked_songs = requestJson['disliked_songs']
            liked_song_ids = "Liked song ID's: "
            disliked_song_ids = "Disliked song ID's: "
            for i in range(len(liked_songs)):
                liked_song_ids += liked_songs[i] + ", "
            for i in range(len(disliked_songs)):
                disliked_song_ids += disliked_songs[i] + ", "
            return liked_song_ids + '\n' + disliked_song_ids
        except Exception as e:
            errorMessage = "Error processing input: {}".format(e)
            return errorMessage

    return app