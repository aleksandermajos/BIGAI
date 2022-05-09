import os
import warnings
import pandas as pd
import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping
import torch

from pytorch_forecasting import Baseline, NBeats, TimeSeriesDataSet
from pytorch_forecasting.data import NaNLabelEncoder
from pytorch_forecasting.data.examples import generate_ar_data
from pytorch_forecasting.metrics import SMAPE

def DF_to_TSDataSet(df_train,df_val, max_encoder_length = 60, max_prediction_length = 20):
    df_train["series"] = 0
    training_cutoff = df_train["time_idx"].max() - max_prediction_length

    context_length = max_encoder_length
    prediction_length = max_prediction_length

    training = TimeSeriesDataSet(
        df_train[lambda x: x.time_idx <= training_cutoff],
        time_idx="time_idx",
        target="pred",
        group_ids=["series"],
        time_varying_unknown_reals=["pred"],
        max_encoder_length=context_length,
        max_prediction_length=prediction_length,
        allow_missing_timesteps=True
    )

    df_val["series"] = 0
    training_cutoff = df_val["time_idx"].max() - max_prediction_length

    context_length = max_encoder_length
    prediction_length = max_prediction_length

    val = TimeSeriesDataSet(
        df_val[lambda x: x.time_idx <= training_cutoff],
        time_idx="time_idx",
        target="pred",
        group_ids=["series"],
        time_varying_unknown_reals=["pred"],
        max_encoder_length=context_length,
        max_prediction_length=prediction_length,
        allow_missing_timesteps=True
    )

    validation = TimeSeriesDataSet.from_dataset(val, df_val)
    batch_size = 128
    train_dataloader = training.to_dataloader(train=True, batch_size=batch_size, num_workers=0)
    val_dataloader = validation.to_dataloader(train=False, batch_size=batch_size, num_workers=0)
    return training, validation, train_dataloader, val_dataloader
