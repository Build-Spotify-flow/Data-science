from flask import Flask, render_template, request
from joblib import load
import pandas as pd
import json
import sqlite3
from .image_parser import radar_chart

pipeline_scaler = load('Models/scaler.joblib')
pipeline_NN = load('Models/NNmodel.joblib')
sqldb = 'Database/Songsdb.sqlite3'


def create_app():
    """Create and configure a basic Flask app"""
    app = Flask(__name__)

    @app.route('/')
    def root():
        return render_template('base.html')

    @app.route('/input', methods=['POST'])
    def retrieval():
        try:
            # Collect all relevant values from request
            requestJson = json.loads(request.data)
            track_id = requestJson['track_id']
            acousticness = float(requestJson['acousticness'])
            danceability = float(requestJson['danceability'])
            duration_ms = int(requestJson['duration_ms'])
            energy = float(requestJson['energy'])
            instrumentalness = float(requestJson['instrumentalness'])
            key = int(requestJson['key'])
            liveness = float(requestJson['liveness'])
            loudness = float(requestJson['loudness'])
            mode = int(requestJson['mode'])
            speechiness = float(requestJson['speechiness'])
            tempo = float(requestJson['tempo'])
            time_signature = int(requestJson['time_signature'])
            valence = float(requestJson['valence'])
            popularity = int(requestJson['popularity'])
            # Place the values in a dataframe
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
            # Generate the radar chart as a base64 string
            radar_base64 = radar_chart(predict_thing)
            # Scale the dataframe from the pickled model
            predict_thing_scaled = pipeline_scaler.transform(predict_thing)
            # Run the nearest neighbor model to output the indices
            # of the 10 recommended songs
            # k=11 because the first value is the input, which we
            # disregard.
            prediction = pipeline_NN.query(predict_thing_scaled, k=11)
            # Make the indices array its own variable
            indices = prediction[1][0].tolist()[1:]
            # Fetch track id's from the SQL database
            conn = sqlite3.connect(sqldb)
            curs = conn.cursor()
            all_data = curs.execute('SELECT track_id from songs;').fetchall()
            curs.close()
            # Convert indices to ID's
            indices_id = list(map(lambda x, y: y[0], indices, all_data))
            # Prepare the output data
            output_data = {
                "radar_chart": radar_base64,
                "recommended_song_ids": indices_id
            }
            # Return the JSON
            return json.dumps(output_data)
        except Exception as e:
            error_message = "Error processing input: {}".format(e)
            return error_message

    return app
