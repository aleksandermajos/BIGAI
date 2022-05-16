from ENGINE.ALL.QM_OHLC_MANIPULATE import MT4_DF_to_CLASSIFICATION
import pandas as pd
from sklearn.model_selection import train_test_split


data = pd.read_csv('DATA\\QM_MT4_CSV\\EURUSD.30.csv')
data = MT4_DF_to_CLASSIFICATION(data)
X_train, X_test, y_train, y_test = train_test_split(data[data.columns[0:4]].values,
                                                    data.Growing.values, test_size=0.2)