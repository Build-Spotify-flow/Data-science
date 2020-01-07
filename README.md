# Data-science
ETL pipeline + Recommender API

## Usage (Production)

Send a POST request to https://spotify-flow-ds.herokuapp.com/input passing in the following JSON object:

```
{
    "liked_songs":[array of song ID's],
    "disliked_songs":[array of song ID's],
}
```

If configured properly, returns back the song ID's (for now).

## Usage (Development)

Clone the repo, then run the following terminal commands within the repo directory.

```
pipenv install
pipenv shell
FLASK_APP=SPOTIFY-FLOW:APP flask run
```

To test the endpoint, create and run the following python code, replacing example song ID's accordingly.

```
import requests
import json
dictToSend = {
    "liked_songs": ["2RM4jf1Xa9zPgMGRDiht8O", "575NJxNUVDqwJGdzBrlLbv", "2FLJcyNuD454zGjSLf6uOk"],
    "disliked_songs": ["2c9ilrzs1RqxnyVVvUybZO", "1N1ZpYUJc9fwrqk53FGgWv"]
}
res = requests.post('http://127.0.0.1:5000/input', data=json.dumps(dictToSend))
print ('RESPONSE FROM SERVER\n' + res.text)
```

(Example song ID's were chosen arbitrarily and do not represent the opinions of the authors.)