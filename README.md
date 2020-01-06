# Data-science
ETL pipeline + Recommender API

## Usage (Production)

Coming soon!

For now, the Flask app returns whatever JSON object you pass.

## Usage (Development)

Clone the repo, then run the following terminal commands within the repo directory.

```
pipenv install
pipenv shell
FLASK_APP=SPOTIFY-FLOW:APP flask run
```

To test the endpoint, create and run the following python code, ~~replacing #'s with relevant numbers~~.

```
import requests
import json
dictToSend = {
    # whatever JSON information you want at the moment
}
res = requests.post('http://127.0.0.1:5000/input', data=json.dumps(dictToSend))
print ('Response from server:',res.text)
```

