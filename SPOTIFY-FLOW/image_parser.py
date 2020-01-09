'''
import base64
import plotly.express as px
import requests # necessary for image generation
from io import BytesIO
from PIL import Image

def radar_chart(radar_dataframe):
    # Extract the 5 features for the radar chart
    features = ['danceability', 'energy', 'instrumentalness', 'speechiness', 'valence']
    plotter = radar_dataframe[features]
    # Create the radar chart
    fig = px.line_polar(plotter, r=plotter.values[0], theta=features, line_close=True,
                    template="plotly_dark", range_r=[0, 1])
    fig.update_traces(fill='toself')
    # Convert the radar chart to a bytes object
    img_bytes = fig.to_image(format="png")
    # Convert bytes object to base64 string that can parse to an image
    img_PIL = Image.open(BytesIO(img_bytes))
    buffered = BytesIO()
    img_PIL.save(buffered, format="png")
    img_str = str(base64.b64encode(buffered.getvalue()).decode("utf-8"))
    return img_str
    '''