# First let's create a Dash application
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from lenspy import DynamicPlot

app = dash.Dash()

# Now let's make a large plot we want to include in the app
x = np.arange(1, 11, 1e-6)
y = 1e-2*np.sin(1e3*x) + np.sin(x) + 1e-3*np.sin(1e10*x)
fig = go.Figure(data=[go.Scattergl(x=x, y=y)])
fig.update_layout(title=f"{len(x):,} Data Points.")

plot = DynamicPlot(fig)

# Use dcc.Graph to create a component with your DynamicPlot
graph_cc = dcc.Graph(id="my_plot",
                     figure=plot.fig,
                     style={"height": "100%", "width": "100%"})

# Add the graph to the app's layout
app.layout = html.Div([graph_cc])

# Create a callback to update the plot on layout changes
app.callback(
    Output("my_plot", "figure"),
    [Input("my_plot", "relayoutData")]
)(plot.refine_plot)

# Run the application
app.run_server()
