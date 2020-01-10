from math import pi
import base64
import io
import matplotlib.pyplot as plt

def radar_chart(radar_dataframe):
    # Extract the 5 features for the radar chart
    features = ['danceability', 'energy', 'instrumentalness', 'speechiness',
                'valence']
    plotter = radar_dataframe[features]
    # Create the radar chart
    with plt.style.context('default'):
      fig = plt.figure()
      categories=list(plotter)
      N = len(categories)
      values=plotter.loc[0].values.flatten().tolist()
      values += values[:1]
      angles = [n / float(N) * 2 * pi for n in range(N)]
      angles += angles[:1]
      ax = plt.subplot(111, polar=True)
      plt.xticks(angles[:-1], categories, color='black', size=10)
      plt.ylim(0,1)
      ax.plot(angles, values, linewidth=1, linestyle='solid', c='black')
      ax.fill(angles, values, '#1DB954', alpha=0.5)
      ax.set_facecolor('xkcd:grey')
    # Convert the radar chart to a bytes object
    pic_IObytes = io.BytesIO()
    fig.savefig(pic_IObytes,  format='png')
    pic_IObytes.seek(0)
    # Convert bytes object to base64 string that can parse to an image
    pic_hash = base64.b64encode(pic_IObytes.read()).decode('utf-8')
    return str(pic_hash)
