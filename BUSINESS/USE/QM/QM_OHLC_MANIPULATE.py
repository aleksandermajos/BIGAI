import numpy as np
import pandas as pd
import itertools


def List_Of_Dict_To_DF(lista):
    lista = list(itertools.chain.from_iterable(lista))

    for i in range(len(lista)):
        lista[i]["O"] = lista[i]["mid"]["o"]
        lista[i]["H"] = lista[i]["mid"]["h"]
        lista[i]["L"] = lista[i]["mid"]["l"]
        lista[i]["C"] = lista[i]["mid"]["c"]
        del lista[i]["mid"]

    df = pd.DataFrame.from_dict(lista)
    del df["complete"]
    df = df[["time","O","H","L","C","volume"]]
    df = OHLCV_AS_NUMBERS(df)
    return df

def OHLCV_AS_NUMBERS(df):
    df["O"] = df["O"].astype(np.float32)
    df["H"] = df["H"].astype(np.float32)
    df["L"] = df["L"].astype(np.float32)
    df["C"] = df["C"].astype(np.float32)
    df["volume"] = df["volume"].astype(np.float32)
    return df

def Df_To_NumPy(df):
    del df["time"]
    return df.iloc[:,0:].values

def Add_Diff_CO_Column(df):
    df["Diff_CO"] = df.C-df.O
    return df

def Add_Growing_Column(df):
    df["Growing"] = df["Diff_CO"] >= 0
    df.Growing.replace((True, False), (1, 0), inplace=True)
    df = df[df.columns.difference(['Diff_CO'])]
    return df

def Df_To_CSV(df,path,name):
    df.to_csv(path+name, index=True)

def Df_Remove_Columns(df, to_remove):
    df_new = df[df.columns.difference(to_remove)]
    return df_new

def OHLC_DF_to_REGRESSION_C(df):
    if "volume" in df:
        df = Df_Remove_Columns(df,["volume"])
    df['time_idx'] = df.index + 0
    if "time" in df:
        df = Df_Remove_Columns(df,["time"])
    if "Diff_CO" in df:
        df = Df_Remove_Columns(df, ["Diff_CO"])
    if "Growing" in df:
        df = Df_Remove_Columns(df, ["Growing"])
    df['pred'] = df.C
    df['pred'] = df['pred'].shift(-1)
    df.drop(df.tail(1).index, inplace=True)
    cols = ['time_idx', 'O', 'H', 'L', 'C', 'pred']
    df = df[cols]
    df = Df_Remove_Columns(df, ["O", "H", "L", "C"])
    return df

def OHLC_DF_to_CLASSIFICATION_C(df):
    df["Diff_CO"] = df.pred - df.C
    df["Growing"] = df["Diff_CO"] >= 0
    df.Growing.replace((True, False), (1, -1), inplace=True)
    df = Df_Remove_Columns(df, ["Diff_CO", "pred"])
    df = df.rename(columns={"Growing": "pred"})
    cols = ['time_idx','O','H', 'L', 'C', 'pred']
    df = df[cols]
    return df

def MT4_DF_to_CLASSIFICATION(df):
    df.columns = ['Data', 'Time', 'O', 'H', 'L', 'C', 'V']
    data = Df_Remove_Columns(df, ['Data', 'Time', 'V'])
    data = Add_Diff_CO_Column(data)
    data = Add_Growing_Column(data)
    data = data.reindex(['O', 'H', 'L', 'C', 'Growing'], axis=1)
    return data