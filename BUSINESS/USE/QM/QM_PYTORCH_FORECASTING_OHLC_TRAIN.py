from BUSINESS.USE.QM.QM_OHLC_MANIPULATE import OHLC_DF_to_REGRESSION_C
from BUSINESS.USE.QM.QM_DF_TO_PYTORCH_FORECASTING import DF_to_TSDataSet
import torch
import pandas as pd
from pytorch_forecasting import Baseline, NBeats
from pytorch_forecasting.metrics import SMAPE

model_path = "C:\\Users\\Aleksander\\PycharmProjects\\BIGAI\\DATALAKE\\MANIPULATION\\AI\\DL\\TIMESERIES\\lightning_logs\\version_3\\checkpoints\\epoch=99-step=1499.ckpt"
best_model = NBeats.load_from_checkpoint(model_path)

data = pd.read_csv('OANDA_EUR_USD_H4.csv')
df = OHLC_DF_to_REGRESSION_C(data)

df_train = df.sample(frac = 0.7)
df_val = df.drop(df_train.index)

training, validation, train_dataloader, val_dataloader = DF_to_TSDataSet(df_train, df_val, max_encoder_length=60,max_prediction_length=1)

actuals = torch.cat([y[0] for x, y in iter(val_dataloader)])

baseline_predictions = Baseline().predict(val_dataloader)
value = SMAPE()(baseline_predictions, actuals)
value = (actuals - baseline_predictions).abs().mean()
predictions = best_model.predict(val_dataloader)
value = (actuals - predictions).abs().mean()
print(value)

raw_predictions, x = best_model.predict(val_dataloader, mode="raw", return_x=True)
oko=3