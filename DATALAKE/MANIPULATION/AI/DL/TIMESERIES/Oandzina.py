import pandas as pd

from Oanda_Data import OandaData
from DATALAKE.MANIPULATION.AI.DL.TIMESERIES.OHLC_Manipulate import OHLC_DF_to_CLASSIFICATION_C, OHLC_DF_to_REGRESSION_C
from DATALAKE.MANIPULATION.AI.DL.TIMESERIES.Data_to_PytorchForecasting import DF_to_TSDataSet
import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping
import torch

from pytorch_forecasting import Baseline, NBeats
from pytorch_forecasting.metrics import SMAPE
'''
OD = OandaData()
data = OD.GetData("2021-10-11T00:00:00Z", "2021-11-11T00:00:00Z", "EUR_USD", "M15", "DF")
'''

data = pd.read_csv('OANDA_EUR_USD_H4.csv')
df = OHLC_DF_to_REGRESSION_C(data)
df_train = df.sample(frac = 0.7)

df_val = df.drop(df_train.index)
training, validation, train_dataloader, val_dataloader = DF_to_TSDataSet(df_train, df_val, max_encoder_length=60,max_prediction_length=1)
actuals = torch.cat([y[0] for x, y in iter(val_dataloader)])


baseline_predictions = Baseline().predict(val_dataloader)
value = SMAPE()(baseline_predictions, actuals)
print(value)


early_stop_callback = EarlyStopping(monitor="val_loss", min_delta=1e-4, patience=10, verbose=False, mode="min")
trainer = pl.Trainer(
    max_epochs=100,
    gpus=0,
    weights_summary="top",
    gradient_clip_val=0.1,
    callbacks=[early_stop_callback],
    limit_train_batches=15,
    # limit_val_batches=1,
    # fast_dev_run=True,
    # logger=logger,
    # profiler=True,
)


net = NBeats.from_dataset(
    training, learning_rate=0.0014125375446227544, log_interval=10, log_val_interval=1, log_gradient_flow=False, weight_decay=1e-2
)
print(f"Number of parameters in network: {net.size()/1e3:.1f}k")

trainer.fit(
    net,
    train_dataloader=train_dataloader,
    val_dataloaders=val_dataloader,
)

best_model_path = trainer.checkpoint_callback.best_model_path
best_model = NBeats.load_from_checkpoint(best_model_path)


actuals = torch.cat([y[0] for x, y in iter(val_dataloader)])
predictions = best_model.predict(val_dataloader)
value = (actuals - predictions).abs().mean()
print(value)