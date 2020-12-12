# LensPy: Plot millions of data points

[![Documentation Status](https://readthedocs.org/projects/lenspy/badge/?version=latest)](https://lenspy.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/lenspy.svg)](https://pypi.python.org/pypi)
![PyPI - License](https://img.shields.io/pypi/l/lenspy)

LensPy extends Plotly's Dash to allow you to plot very large datasets (millions of points) while ensuring that figures are still fast, fluid, and responsive.

![alt text](https://github.com/serant/lenspy/blob/master/img/demo.gif?raw=true)

This is achieved by adjusting the visible data based on the position of the viewport and how _zoomed in_ the figure is. When you're zoomed out, only a subset of the data is shown. When you zoom in, LensPy will render more detail in your plot. By doing this, LensPy can build dynamic figures of very large datasets without overwhelming the browser when viewing the figures.

## Contents

- [Features](#features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Jupyter](#jupyter)
- [Advanced Usage](#advanced-usage)
- [License](#license)
- [Contributing](#contributing)

## Features

- Ability to specify number of points to display at once
- Ability to define a custom function for downsampling data
- Ability to run in [Jupyter](#jupyter) notebooks
- Ability to use with Dash applications

## Installation

Install LensPy using pip

```
pip install lenspy
```

## Getting Started

Use LensPy by passing any [Figure](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html) to the DynamicPlot constructor.

```
import numpy as np
import plotly.graph_objects as go
from lenspy import DynamicPlot

# First, let's create a very large figure
x = np.arange(1, 11, 1e-6)
y = 1e-2*np.sin(1e3*x) + np.sin(x) + 1e-3*np.sin(1e10*x)
fig = go.Figure(data=[go.Scattergl(x=x, y=y)])
fig.update_layout(title=f"{len(x):,} Data Points.")

# Use DynamicPlot.show to view the plot
plot = DynamicPlot(fig)
plot.show()

# Plot will be available in the browser at http://127.0.0.1:8050/
```

![alt text](https://github.com/serant/lenspy/blob/master/img/demo2.gif?raw=true)

You can still access any of the [Plotly Figure methods/attributes](https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html) and modify them as needed.

## Jupyter

LensPy starts a [Flask](https://flask.palletsprojects.com/en/1.1.x/) web server, therefore plots won't be rendered in your notebook as widget. You can always access your plot in a seperate tab (default url is http://127.0.0.1:8050/)

## Advanced Usage

For the full reference and detailed information, please see the [documentation](https://lenspy.readthedocs.io/en/latest/).

## License

Copyright (c) 2020 Seran Thirugnanam under the MIT License.

## Contributing

Help is always welcome. Feel free to open issues or PRs if there is a feature missing, or a bug to be addressed.
