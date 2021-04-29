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
    df.Growing.replace((True, False), (1, -1), inplace=True)
    return df

def Df_To_CSV(df,path,name):
    df.to_csv(path+name, index=True)

def Df_Remove_Columns(df, to_remove):
    return df[df.columns.difference(to_remove)]

def OHLC_DF_to_REGRESSION(df):
    pass