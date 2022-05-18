import pandas as pd
from urllib.error import HTTPError


def get_iris_dataset():
    try:
        s = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
        print('From URL:', s)
        df = pd.read_csv(s,
                         header=None,
                         encoding='utf-8')

    except HTTPError:
        s = 'iris.data'
        print('From local Iris path:', s)
        df = pd.read_csv(s,
                         header=None,
                         encoding='utf-8')

    return df