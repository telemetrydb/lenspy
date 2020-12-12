import pandas as pd
import plotly.express as px
from lenspy import DynamicPlot

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv')
fig = px.density_mapbox(df,
                        lat='Latitude',
                        lon='Longitude',
                        z='Magnitude',
                        radius=10,
                        center=dict(lat=0, lon=180),
                        zoom=0,
                        mapbox_style="stamen-terrain")

plot = DynamicPlot(fig)
plot.show()
