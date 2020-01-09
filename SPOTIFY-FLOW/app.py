from flask import Flask, render_template, request
from joblib import load
import pandas as pd
import json
import sqlite3

pipelineScaler = load('Models/scaler.joblib')
pipelineNN = load('Models/NNmodel.joblib')
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
            # Scale the dataframe from the pickled model
            predictionScaled = pipelineScaler.transform(predict_thing)
            # Run the nearest neighbor model to output the indices
            # of the 10 recommended songs
            # k=11 because the first value is the input, which we
            # disregard.
            prediction = pipelineNN.query(predictionScaled, k=11)
            # Make the indices array its own variable
            indices = prediction[1][0].tolist()[1:]
            # Fetch track id's from the SQL database
            conn = sqlite3.connect(sqldb)
            curs = conn.cursor()
            allData = curs.execute('SELECT track_id from songs;').fetchall()
            curs.close()
            # Convert indices to ID's
            indicesIDs = list(map(lambda x, y: y[0], indices, allData)) 
            # Prepare the output data
            outputData = {
                "radar_chart": "not ready yet",
                "recommended_song_ids": []
            }
            outputData['recommended_song_ids'] = indicesIDs
            # Return the JSON
            return json.dumps(outputData)
        except Exception as e:
            errorMessage = "Error processing input: {}".format(e)
            return errorMessage

    return app