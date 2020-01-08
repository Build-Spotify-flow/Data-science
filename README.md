# Data-science
ETL pipeline + Recommender API

**Please note: The Flask app does not work based on this documentation yet!**

## Usage (Production)

The Flask app returns 10 recommended songs based on one song's features.

Send a POST request to `https://spotify-flow-ds.herokuapp.com/input` passing in a JSON object of this structure:

```
{
    "track_id": "track id",
    "acousticness": #,
    "danceability": #,
    "duration_ms": #,
    "energy": #,
    "instrumentalness": #,
    "key": #,
    "liveness": #,
    "loudness": #,
    "mode": #,
    "speechiness": #,
    "tempo": #,
    "time_signature": #,
    "valence": #,
    "popularity": #
}
```

If configured properly, returns:

```
{
    "radar_chart": "radar chart of inputted song^",
    "recommended_song_ids": [array of 10 song IDs]
}
```

^ A base64-encoded image. The radar chart uses the following features:

* danceability
* energy
* instrumentalness
* speechiness
* valence

## Usage (Development)

Clone the repo, then run the following terminal commands within the repo directory.

```
pipenv install
pipenv shell
FLASK_APP=SPOTIFY-FLOW:APP flask run
```

To test the endpoint, create and run the following python code, replacing example JSON values accordingly.

```
import requests
import json
dictToSend = {
    "track_id": "2RM4jf1Xa9zPgMGRDiht8O",
    "acousticness": 0.00582,
    "danceability": 0.743,
    "duration_ms": 238373,
    "energy": 0.339,
    "instrumentalness": 0,
    "key": 1,
    "liveness": 0.0812,
    "loudness": -7.678,
    "mode": 1,
    "speechiness": 0.409,
    "tempo": 203.927,
    "time_signature": 4,
    "valence": 0.118,
    "popularity": 15
}
res = requests.post('http://127.0.0.1:5000/input', data=json.dumps(dictToSend))
print ('RESPONSE FROM SERVER\n' + res.text)
```