import logging
from functools import reduce
from multiprocessing import Process
from typing import Dict, List, Optional, Tuple, Union

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from plotly.basedatatypes import BaseTraceType


class TraceManager():
    """Manages the content of a Trace based on the viewport of the :class:`plotly.graph_objects.Figure`.

    Configure the number of points to show at any given time using :param max_points:. ``agg_func``, 
    ``agg_args``, and ``agg_kwargs`` are passed directly to :meth:`pd.core.groupby.DataFrameGroupby.aggregate`.

    :param trace: The trace to be managed.
    :type trace: class:`plotly.basedatatypes.BaseTraceType`

    :param max_points: The maximum number of points to display at any given point, defaults to 10,240
    :type max_points: int, optional

    :param agg_func: The function to aggregate the trace with
    :type agg_func: str or callable

    :param agg_args: Arguments to pass to ``agg_func``
    :type agg_args: tuple

    :param agg_kwargs: Keyword arguments to pass to ``agg_func``
    :type agg_kwargs: dict

    """

    def __init__(self,
                 trace: BaseTraceType,
                 max_points: int,
                 agg_func: Union[str, List, Dict],
                 agg_args: Tuple,
                 agg_kwargs: Dict):
        """Constructor for :class:`.TraceManager`.
        """
        self.max_points = max_points

        self.agg_func = agg_func
        self.agg_args = agg_args
        self.agg_kwargs = agg_kwargs

        self.trace = trace
        self.trace_df, self.dimensions = self.extract_df(trace)

    def extract_df(self, trace: BaseTraceType) -> Tuple[pd.DataFrame, List[str]]:
        """Extracts the data passed to the trace and returns a pd.DataFrame.

        :param trace: The trace to be managed
        :type trace: class:`plotly.basedatatypes.BaseTraceType`

        :return: Tuple containing the :class:`pd.DataFrame` and a list of the dimensions to include in the plot
        :rtype: tuple
        """
        # Do not populate DF in constructor, so that we
        # don't make redundant copies of the data

        # When building the dataframe, search all the attributes
        # to find the ones that are arrays
        df = pd.DataFrame()

        # Add all array type attrs to the dataframe
        for attr_name in dir(trace):
            if attr_name.startswith("_"):
                continue
            attr = getattr(trace, attr_name)
            if type(attr) in [tuple, list, np.ndarray, pd.Series]:
                df[attr_name] = attr

        axis_names = ["x", "y", "z", "lon", "lat"]
        plot_dimensions = [d for d in axis_names if d in df.columns]

        return df, plot_dimensions

    def refresh(self, view_port: Dict[str, Union[int, float]] = {}):
        """Updates the trace based on the viewport.

        :param view_port: Viewport to update the trace with. Defaults to {}
        :type view_port: dict, optional
        """
        # Determine the dimensions of the trace in relation to the viewport
        vp = view_port

        dims = [d for d in self.dimensions if vp.get(
            f"{d}1", None) is not None]

        if not dims:
            t_slice = self.trace_df
        else:
            filts = [((self.trace_df[d] >= vp[f"{d}1"]) &
                      (self.trace_df[d] <= vp[f"{d}2"]))
                     for d in dims]

            filts = reduce(lambda x, y: x & y, filts)
            t_slice = self.trace_df[filts]

        n = max(round(t_slice.shape[0] / self.max_points), 1)

        resampler = np.arange(len(t_slice)) // n

        t_slice = t_slice\
            .groupby(resampler)\
            .agg(self.agg_func, *self.agg_args, **self.agg_kwargs)

        # Finally, update the trace attrs
        for d in t_slice.columns:
            setattr(self.trace, d, t_slice[d])


class DynamicPlot():
    @property
    def max_points(self):
        return self._max_points

    @max_points.setter
    def max_points(self, value: int):
        self._max_points = value

    def __init__(self,
                 fig: go.Figure,
                 max_points: Optional[int] = 10_240,
                 agg_func: Optional[Union[str, List, Dict]] = "first",
                 agg_args: Tuple = (),
                 agg_kwargs: Dict = {}):
        """Wraps a :class:`plotly.graph_objects.Figure` object with a renderer which aggregates data
        based on the viewport.

        Configure the number of points to show at any given time using ``max_points``.

        ``agg_func``, ``agg_args``, and ``agg_kwargs`` are passed directly to
        :meth:`pandas.core.groupby.DataFrameGroupby.aggregate`.

        :param fig: The figure to render.
        :type fig: :class:`plotly.graph_objects.Figure`

        :param max_points: The number of points to display at any given point. Defaults to 10,240
        :type max_points: int, optional

        :param agg_func: The function to aggregate the trace with. Defaults to "first"
        :type agg_func: callable or str supported by :meth:`pandas.core.groupby.DataFrameGroupby.aggregate`

        :param agg_args: Arguments to pass to ``agg_func``
        :type agg_args: tuple

        :param agg_kwargs: Keyword arguments to pass to ``agg_func``
        :type agg_kwargs: dict
        """
        self.fig = fig

        self.agg_func = agg_func
        self.agg_args = agg_args
        self.agg_kwargs = agg_kwargs

        self.max_points = max_points

        self.trace_managers = [
            TraceManager(t,
                         max_points=self.max_points,
                         agg_func=agg_func,
                         agg_args=agg_args,
                         agg_kwargs=agg_kwargs)
            for t in fig.data]

        self._refresh_traces()
        self.app = self._build_app()

    def set_aggregator(self,
                       agg_func: Optional[Union[str, List, Dict]] = "first",
                       agg_args: Tuple = (),
                       agg_kwargs: Dict = {}):
        """Updates the aggregator.

        :param agg_func: The function to aggregate the trace with. Defaults to "first"
        :type agg_func: callable or str supported by :meth:`pandas.core.groupby.DataFrameGroupby.aggregate`

        :param agg_args: Arguments to pass to ``agg_func``
        :type agg_args: tuple

        :param agg_kwargs: Keyword arguments to pass to ``agg_func``
        :type agg_kwargs: dict
        """
        self.agg_func = func
        self.agg_args = args
        self.agg_kwargs = kwargs

    def _refresh_traces(self, view_port: Dict[str, Union[int, float]] = {}):
        # Resample all traces to maintain the resolution
        for trace in self.trace_managers:
            trace.refresh(view_port)

    def _build_app(self) -> dash.Dash:
        app = dash.Dash()

        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        app.layout = html.Div([
            dcc.Graph(id="main_plot", figure=self.fig,
                      style={"height": "100%", "width": "100%"})
        ], style={"height": "100vh"})

        @ app.callback(
            Output("main_plot", "figure"),
            [Input("main_plot", "relayoutData")]
        )
        def refine_plot(relayoutData):
            rl = relayoutData or {}

            # Cartesian
            if "xaxis.range[0]" in rl:
                vw = {
                    "x1": rl.get("xaxis.range[0]"),
                    "x2": rl.get("xaxis.range[1]"),

                    "y1": rl.get("yaxis.range[0]"),
                    "y2": rl.get("yaxis.range[1]"),

                    "z1": rl.get("zaxis.range[0]"),
                    "z2": rl.get("zaxis.range[1]"),
                }

            elif "mapbox._derived" in rl:
                lon1 = min(c[0] for c in rl["mapbox._derived"]["coordinates"])
                lon2 = max(c[0] for c in rl["mapbox._derived"]["coordinates"])

                lat1 = min(c[1] for c in rl["mapbox._derived"]["coordinates"])
                lat2 = max(c[1] for c in rl["mapbox._derived"]["coordinates"])
                vw = {
                    "lon1": lon1,
                    "lon2": lon2,
                    "lat1": lat1,
                    "lat2": lat2,
                }

                # Update the layout properties
                new_layout = {
                    k: v for k, v in rl.items() if not any([i.startswith("_") for i in k.split('.')])
                }
                self.fig.update_layout(new_layout)

            else:
                vw = {}

            self._refresh_traces(vw)

            return self.fig

        return app

    def show(self, *args, **kwargs):
        """Displays the plot. All arguments are passed to :meth:`dash.Dash.run_server`
        """
        self.app.run_server(*args, **kwargs)
