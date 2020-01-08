from flask import Flask, render_template, request
from joblib import load
import pandas as pd
import json

pipelineScaler = load('Models/scaler.joblib')
pipelineNN = load('Models/NNmodel.joblib')

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
            track_id = requestJson['track_id']
            acousticness = float(requestJson['acousticness'])
            danceability = float(requestJson['danceability'])
            duration_ms = int(requestJson['duration_ms'])
            energy = float(requestJson['energy'])
            instrumentalness = float(requestJson['instrumentalness'])
            danceability = float(requestJson['danceability'])
            key = int(requestJson['key'])
            liveness = float(requestJson['liveness'])
            loudness = float(requestJson['loudness'])
            mode = int(requestJson['mode'])
            speechiness = float(requestJson['speechiness'])
            tempo = float(requestJson['tempo'])
            time_signature = int(requestJson['time_signature'])
            valence = float(requestJson['valence'])
            popularity = int(requestJson['popularity'])
            predict_thing = pd.DataFrame(
                columns=['acousticness', 'danceability', 'duration_ms',
                         'energy', 'instrumentalness', 'key', 'liveness',
                         'loudness', 'mode', 'speechiness', 'tempo',
                         'time_signature', 'valence', 'popularity'],
                data=[[acousticness, danceability, duration_ms,
                      energy, instrumentalness, key, liveness,
                      loudness, mode, speechiness, tempo, 
                      time_signature, valence, popularity]]
                )
            predictionScaled = pipelineScaler.transform(predict_thing)
            prediction = pipelineNN.query(predictionScaled, k=11)
            indices = prediction[1][0].tolist()[1:]
            return str(indices)
        except Exception as e:
            errorMessage = "Error processing input: {}".format(e)
            return errorMessage

    return app