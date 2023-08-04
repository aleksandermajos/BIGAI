from ENGINE.DATA_OHLC_MANIPULATE import Df_Remove_Columns
from ENGINE.DATA_OHLC_MANIPULATE import Add_Growing_Column, Add_Diff_CO_Column


def MT4_DF_to_CLASSIFICATION(df):
    df.columns = ['Data', 'Time', 'O', 'H', 'L', 'C', 'V']
    data = Df_Remove_Columns(df, ['Data', 'Time', 'V'])
    result = data.dtypes
    data = Add_Diff_CO_Column(data)
    data = Add_Growing_Column(data)
    data = data.reindex(['O', 'H', 'L', 'C', 'Growing'], axis=1)
    return data

def MT5_DF_to_CLASSIFICATION(df):
    df.columns = ['Data', 'Time', 'O', 'H', 'L', 'C', 'TV', 'V', 'S']
    data = Df_Remove_Columns(df, ['Data', 'Time', 'TV', 'V', 'S'])
    data['O'] = df['O'].astype(float)
    data['H'] = df['H'].astype(float)
    data['L'] = df['L'].astype(float)
    data['C'] = df['C'].astype(float)
    result = data.dtypes
    data = Add_Diff_CO_Column(data)
    data = Add_Growing_Column(data)
    data = data.reindex(['O', 'H', 'L', 'C', 'Growing'], axis=1)
    return data

def cTRADER_DF_to_CLASSIFICATION(df):
    df.columns = ['DataTime', 'O', 'H', 'L', 'C', 'V']
    data = Df_Remove_Columns(df, ['DataTime', 'V'])
    data['O'] = df['O'].astype(float)
    data['H'] = df['H'].astype(float)
    data['L'] = df['L'].astype(float)
    data['C'] = df['C'].astype(float)
    result = data.dtypes
    data = Add_Diff_CO_Column(data)
    data = Add_Growing_Column(data)
    data = data.reindex(['O', 'H', 'L', 'C', 'Growing'], axis=1)
    return data