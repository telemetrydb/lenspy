import plotly.express as px
import pandas as pd
from eventful import DynamicPlot

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/uber-rides-data1.csv')
dff = df.query('Lat < 40.82').query('Lat > 40.70').query(
    'Lon > -74.02').query('Lon < -73.91')

# Trick to create rapidly a figure with mapbox axes
fig = px.scatter_mapbox(dff, lat='Lat', lon='Lon', zoom=12)
# Add the datashader image as a mapbox layer image

fig.update_layout(mapbox_style="carto-darkmatter")

plot = DynamicPlot(fig)
plot.show()
