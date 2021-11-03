import torch
from torch import nn
from typing import Dict
import numpy as np
import pandas as pd
from pytorch_forecasting.models import BaseModel
from pytorch_forecasting import TimeSeriesDataSet
from torch.utils.data import WeightedRandomSampler
from pytorch_forecasting.data.encoders import NaNLabelEncoder
from pytorch_forecasting.metrics import CrossEntropy
from pytorch_forecasting.data.encoders import EncoderNormalizer, MultiNormalizer, TorchNormalizer


class FullyConnectedModule(nn.Module):
    def __init__(self, input_size: int, output_size: int, hidden_size: int, n_hidden_layers: int):
        super().__init__()

        # input layer
        module_list = [nn.Linear(input_size, hidden_size), nn.ReLU()]
        # hidden layers
        for _ in range(n_hidden_layers):
            module_list.extend([nn.Linear(hidden_size, hidden_size), nn.ReLU()])
        # output layer
        module_list.append(nn.Linear(hidden_size, output_size))

        self.sequential = nn.Sequential(*module_list)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x of shape: batch_size x n_timesteps_in
        # output of shape batch_size x n_timesteps_out
        return self.sequential(x)


class FullyConnectedModel(BaseModel):
    def __init__(self, input_size: int, output_size: int, hidden_size: int, n_hidden_layers: int, **kwargs):
        # saves arguments in signature to `.hparams` attribute, mandatory call - do not skip this
        self.save_hyperparameters()
        # pass additional arguments to BaseModel.__init__, mandatory call - do not skip this
        super().__init__(**kwargs)
        self.network = FullyConnectedModule(
            input_size=self.hparams.input_size,
            output_size=self.hparams.output_size,
            hidden_size=self.hparams.hidden_size,
            n_hidden_layers=self.hparams.n_hidden_layers,
        )

    def forward(self, x: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        # x is a batch generated based on the TimeSeriesDataset
        network_input = x["encoder_cont"].squeeze(-1)
        prediction = self.network(network_input)

        # We need to return a dictionary that at least contains the prediction and the target_scale.
        # The parameter can be directly forwarded from the input.
        return dict(prediction=prediction, target_scale=x["target_scale"])

    def from_dataset(cls, dataset: TimeSeriesDataSet, **kwargs):
        new_kwargs = {
            "output_size": dataset.max_prediction_length,
            "input_size": dataset.max_encoder_length,
        }
        new_kwargs.update(kwargs)  # use to pass real hyperparameters and override defaults set by dataset
        # example for dataset validation
        assert dataset.max_prediction_length == dataset.min_prediction_length, "Decoder only supports a fixed length"
        assert dataset.min_encoder_length == dataset.max_encoder_length, "Encoder only supports a fixed length"
        assert (
                len(dataset.time_varying_known_categoricals) == 0
                and len(dataset.time_varying_known_reals) == 0
                and len(dataset.time_varying_unknown_categoricals) == 0
                and len(dataset.static_categoricals) == 0
                and len(dataset.static_reals) == 0
                and len(dataset.time_varying_unknown_reals) == 1
                and dataset.time_varying_unknown_reals[0] == dataset.target
        ), "Only covariate should be the target in 'time_varying_unknown_reals'"

        return super().from_dataset(dataset, **new_kwargs)
multi_target_test_data = pd.DataFrame(
    dict(
        target1=np.random.rand(30),
        target2=np.random.rand(30),
        group=np.repeat(np.arange(3), 10),
        time_idx=np.tile(np.arange(10), 3),
    )
)

# create the dataset from the pandas dataframe
# create the dataset from the pandas dataframe
multi_target_dataset = TimeSeriesDataSet(
    multi_target_test_data,
    group_ids=["group"],
    target=["target1", "target2"],  # USING two targets
    time_idx="time_idx",
    min_encoder_length=5,
    max_encoder_length=5,
    min_prediction_length=2,
    max_prediction_length=2,
    time_varying_unknown_reals=["target1", "target2"],
    target_normalizer=MultiNormalizer(
        [EncoderNormalizer(), TorchNormalizer()]
    ),  # Use the NaNLabelEncoder to encode categorical target
)

x, y = next(iter(multi_target_dataset.to_dataloader(batch_size=4)))
y[0]  # target values are a list of targets
