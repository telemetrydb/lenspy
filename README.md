# LensPy: Plot millions of datapoints
[![Documentation Status](https://readthedocs.org/projects/lenspy/badge/?version=latest)](https://lenspy.readthedocs.io/en/latest/?badge=latest)

LensPy extends Plotly's Dash to allow you to plot very large datasets (millions of points) while ensuring that figures are still fast, fluid, and responsive.

![alt text](https://github.com/serant/lenspy/blob/main/img/demo.gif?raw=true)

This is achieved by adjusting the visible data based on the position of the viewport and how _zoomed in_ the figure is. When you're zoomed out, only a subset of the data is shown. When you zoom in, LensPy will render more detail in your plot. By doing this, LensPy can build dynamic figures of very large datasets without overwhelming the browser when viewing the figures.

## Features

- Support for the majority Plotly trace types
- Ability to specify number of points to display at once
- Ability to define a custom function for downsampling data
- Ability to run in Jupyter notebooks (see Getting Started: Jupyter for more information)

## Installation

Install LensPy using pip

```
pip install lenspy
```

## Getting Started

Use LensPy by passing any [Figure](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html) to the DynamicPlot constructor.

```
fig = go.Figure(
        data=[go.Scatter(x=df["timestamp"],
                         y=df["close"],
                         name="close")])

plot = DynamicPlot(fig)
plot.show()

# Plot will be available in the browser at http://127.0.0.1:8050/
```

You can still access any of the [Plotly Figure methods/attributes](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html) and modify them as needed.

### Jupyter

LensPy starts a [Flask](https://flask.palletsprojects.com/en/1.1.x/) web server, therefore plots won't be rendered in your notebook as widget. You can always access your plot in a seperate tab (default url is http://127.0.0.1:8050/)

### Overriding Flask Arguments

Any argumetns passed to `DynamicPlot.show` will be passed to App.run_server for [Plotly's Dash](https://dash.plotly.com). You can use this to change the endpoint that they plot is hosted at.

```
plot = DynamicPlot(fig)
plot.show(port="8051")
# Plot will be available in the browser at http://127.0.0.1:8051/ instead of http://127.0.0.1:8050/
```

### Custom Resolution

You can change the maximum number of points rendered at any given point by setting a value for `max_points` when creating an instance of `DynamicPlot`. The default value is 10,240 points.

```
# Display a plot that only shows a maximum of 1,000 points at a time.

plot = DynamicPlot(fig, max_points=1000)
plot.show()
```

You may need to adjust this parameter based on your hardware.

### Custom Aggregators

The default method for downsampling the graph is to use the _first_ point of each downsampled group. You can override this functionality by specifying a different aggregator.

```
plot = DynamicPlot(fig, agg_func="avg")
plot.show()
```

The `agg_func` parameter is used by [Panda's GroupBy aggregate method](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.core.groupby.DataFrameGroupBy.aggregate.html). Any valid Panda's GroupBy _func_ will work.

### Blocking Plots

Unlike standard Plotly plots, DynamicPlot.show() is a blocking function. Therefore, if running in a Jupyter notebook, or in a script, the `show` method will block indefinitely.

### Documentation

For the full reference and detailed information, please see the [documentation](https://lenspy.readthedocs.io/en/latest/).

## License

Copyright (c) 2020 Seran Thirugnanam under the MIT License.

## Contributing

Help is always welcome. Feel free to open issues or PRs if there is a feature missing, or a bug to be addressed.
