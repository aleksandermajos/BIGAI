import plotly.graph_objects as go

def candle_OHLC(data_df):
    fig = go.Figure(data=[go.Candlestick(open=data_df['O'],
                                         high=data_df['H'],
                                         low=data_df['L'],
                                         close=data_df['C'])])

    return fig