Quick Start
===========

Installation
------------

Install LensPy using pip

.. code-block:: bash

  pip install lenspy

Basic Usage
-----------

Use LensPy by passing any `Figure <https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html>`_ to the DynamicPlot constructor.

.. code-block:: python

  fig = go.Figure(
          data=[go.Scatter(x=df["timestamp"],
                          y=df["close"],
                          name="close")])

  plot = DynamicPlot(fig)
  plot.show()

  # Plot will be available in the browser at http://127.0.0.1:8050/

You can still access any of the `Plotly Figure methods/attributes <https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html>`_ and modify them as needed.

Jupyter
-------

LensPy starts a `Flask <https://flask.palletsprojects.com/en/1.1.x/>`_ web server, therefore plots won't be rendered in your notebook as widget. You can always access your plot in a seperate tab (default url is http://127.0.0.1:8050/)

Overriding Flask Arguments
--------------------------

Any arguments passed to `DynamicPlot.show` will be passed to App.run_server for `Plotly's Dash <https://dash.plotly.com>`_. You can use this to change the endpoint that they plot is hosted at.

.. code-block:: python

  plot = DynamicPlot(fig)
  plot.show(port="8051")
  # Plot will be available in the browser at http://127.0.0.1:8051/ instead of http://127.0.0.1:8050/


Custom Resolution
-----------------

You can change the maximum number of points rendered at any given point by setting a value for `max_points` when creating an instance of `DynamicPlot`. The default value is 10,240 points.

.. code-block:: python

  # Display a plot that only shows a maximum of 1,000 points at a time.

  plot = DynamicPlot(fig, max_points=1000)
  plot.show()

You may need to adjust this parameter based on your hardware.

Custom Aggregators
------------------

The default method for downsampling the graph is to use the *first* point of each downsampled group. You can override this functionality by specifying a different aggregator.

.. code-block:: python

  plot = DynamicPlot(fig, agg_func="avg")
  plot.show()


The `agg_func` parameter is used by `Pandas' GroupBy aggregate method <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.core.groupby.DataFrameGroupBy.aggregate.html>`_. Any valid Panda's GroupBy func will work.

Blocking Plots
--------------

Unlike standard Plotly plots, DynamicPlot.show() is a blocking function. Therefore, if running in a Jupyter notebook, or in a script, the `show` method will block indefinitely.
