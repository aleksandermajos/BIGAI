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
training, train_dataloader, val_dataloader = DF_to_TSDataSet(df)
#actuals = torch.cat([y[0] for x, y in iter(val_dataloader)])
#baseline_predictions = Baseline().predict(val_dataloader)
#value = SMAPE()(baseline_predictions, actuals)
#print(value)


early_stop_callback = EarlyStopping(monitor="val_loss", min_delta=1e-4, patience=10, verbose=False, mode="min")
trainer = pl.Trainer(
    max_epochs=100,
    gpus=[0],
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
    training, learning_rate=3e-2, log_interval=10, log_val_interval=1, log_gradient_flow=False, weight_decay=1e-2
)
print(f"Number of parameters in network: {net.size()/1e3:.1f}k")

trainer.fit(
    net,
    train_dataloader=train_dataloader,
    val_dataloaders=val_dataloader,
)