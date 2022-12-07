import numpy as np
import pandas as pd
from ENGINE.DATA_OHLC_MANIPULATE import MT4_DF_to_CLASSIFICATION
from ENGINE.DATA_OHLC_MANIPULATE import MT5_DF_to_CLASSIFICATION
from ENGINE.DATA_OHLC_MANIPULATE import cTRADER_DF_to_CLASSIFICATION


def MT4_CSV_TO_CLASSIFICATION(path,window):
    df = pd.read_csv(path)
    df = MT4_DF_to_CLASSIFICATION(df)
    df['Growing'] = df['Growing'].shift(-1)
    df = df.iloc[:-1]
    X_init = df.loc[:, 'O':'C'].values
    X = np.zeros([len(df)-window, 4*window],dtype=float)
    Y_init = df.loc[:,'Growing':'Growing'].values
    Y = np.zeros([len(df) - window,1], dtype=float)
    window_nr =0
    for _ in range(len(df)-window):
        current_x = X_init[window_nr:window_nr+window].ravel()
        X[window_nr] = current_x
        current_y = Y_init[window_nr+window-1]
        Y[window_nr] = current_y

        window_nr += 1

    return X, Y

def MT5_CSV_TO_CLASSIFICATION(path,window):
    df = pd.read_csv(path, sep='\s+', header=None)
    df.drop(index=df.index[0],axis=0,inplace=True)
    df = MT5_DF_to_CLASSIFICATION(df)
    df['Growing'] = df['Growing'].shift(-1)
    df = df.iloc[:-1]
    X_init = df.loc[:, 'O':'C'].values
    X = np.zeros([len(df)-window, 4*window],dtype=float)
    Y_init = df.loc[:,'Growing':'Growing'].values
    Y = np.zeros([len(df) - window,1], dtype=float)
    window_nr =0
    for _ in range(len(df)-window):
        current_x = X_init[window_nr:window_nr+window].ravel()
        X[window_nr] = current_x
        current_y = Y_init[window_nr+window-1]
        Y[window_nr] = current_y

        window_nr += 1

    return X, Y

def cTRADER_CSV_TO_CLASSIFICATION(path,window):
    df = pd.read_csv(path, header=None)
    df.drop(index=df.index[0],axis=0,inplace=True)
    df = cTRADER_DF_to_CLASSIFICATION(df)
    df['Growing'] = df['Growing'].shift(-1)
    df = df.iloc[:-1]
    X_init = df.loc[:, 'O':'C'].values
    X = np.zeros([len(df)-window, 4*window],dtype=float)
    Y_init = df.loc[:,'Growing':'Growing'].values
    Y = np.zeros([len(df) - window,1], dtype=float)
    window_nr =0
    for _ in range(len(df)-window):
        current_x = X_init[window_nr:window_nr+window].ravel()
        X[window_nr] = current_x
        current_y = Y_init[window_nr+window-1]
        Y[window_nr] = current_y

        window_nr += 1

    return X, Y