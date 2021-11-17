from DATALAKE.MANIPULATION.AI.DL.TIMESERIES.OHLC_Manipulate import OHLC_DF_to_CLASSIFICATION_C, OHLC_DF_to_REGRESSION_C
from DATALAKE.MANIPULATION.AI.DL.TIMESERIES.Data_to_PytorchForecasting import DF_to_TSDataSet
import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping
import torch

from pytorch_forecasting import Baseline, NBeats
from pytorch_forecasting.metrics import SMAPE
import pandas as pd

df = pd.read_csv('OANDA_EUR_USD_H4.csv')
df = OHLC_DF_to_REGRESSION_C(df)


