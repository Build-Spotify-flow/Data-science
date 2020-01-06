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
            return requestJson
        except Exception as e:
            errorMessage = "Error processing input: {}".format(e)
            return errorMessage

    return app