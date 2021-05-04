from Oanda_Data import OandaData
from ENGINE.DATALAKE.TIMESERIES.OHLC_Manipulate import OHLC_DF_to_REGRESSION_C, OHLC_DF_to_CLASSIFICATION_C
from ENGINE.DATALAKE.TIMESERIES.Data_to_PytorchForecasting import DF_to_TSDataSet
import pandas as pd
import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping
import torch

from pytorch_forecasting import Baseline, NBeats, TimeSeriesDataSet
from pytorch_forecasting.data import NaNLabelEncoder
from pytorch_forecasting.data.examples import generate_ar_data
from pytorch_forecasting.metrics import SMAPE
OD = OandaData()
data = OD.GetData("2021-01-01T00:00:00Z", "2021-04-21T00:00:00Z", "EUR_USD", "M15", "DF")
df = OHLC_DF_to_REGRESSION_C(data)
train_dataloader, val_dataloader = DF_to_TSDataSet(df)
actuals = torch.cat([y[0] for x, y in iter(val_dataloader)])
baseline_predictions = Baseline().predict(val_dataloader)
value = SMAPE()(baseline_predictions, actuals)
print(value)