import pandas as pd
import plotly.graph_objects as go
from eventful import DynamicPlot
import os


def import_data(data_path: str) -> pd.DataFrame:
    df = pd.read_pickle(data_path)

    df.sort_values(by="timestamp", inplace=True)
    # df["timestamp"] = pd.to_numeric(df["timestamp"])

    return df


def get_fig(df: pd.DataFrame):
    fig = go.Figure(
        data=[go.Scatter(x=df["timestamp"],
                         y=df["close"],
                         name="close")])

    fig.update_layout(title=f"Stock Price Every Minute ({len(df)} points)",
                      yaxis_title='Stock Price (USD)')

    return fig


# if __name__ == "__main__":
#     script_dir = os.path.dirname(".")
#     data_path = os.path.join(script_dir, "data", "sample_stock_data.pkl")
#     df = import_data(data_path)
#     fig = get_fig(df)
#     plot = DynamicPlot(fig)
#     plot.show()
#     plot.show(port="8051")
