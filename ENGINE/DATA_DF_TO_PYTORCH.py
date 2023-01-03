from sklearn.preprocessing import StandardScaler
from torch.autograd import Variable
import torch
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from pytorch_forecasting import Baseline, NBeats, TimeSeriesDataSet
from pytorch_forecasting.data import NaNLabelEncoder
from pytorch_forecasting.data.examples import generate_ar_data
from pytorch_forecasting.metrics import SMAPE


def DF_TO_PYTORCH(X,Y,test_size,scaler):
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = test_size, random_state = 42)
    if scaler:
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)

    X_train = Variable(torch.from_numpy(X_train)).float()
    y_train = Variable(torch.from_numpy(y_train)).float()
    X_test = Variable(torch.from_numpy(X_test)).float()
    y_test = Variable(torch.from_numpy(y_test)).float()

    return X_train, y_train, X_test, y_test

def DF_TO_PYTORCH_DATASET(X,Y,test_size,scaler,batch_size,drop_last,shuffle):
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = test_size, random_state = 42)
    if scaler:
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)

    X_train = Variable(torch.from_numpy(X_train)).float()
    y_train = Variable(torch.from_numpy(y_train)).float()
    X_test = Variable(torch.from_numpy(X_test)).float()
    y_test = Variable(torch.from_numpy(y_test)).float()

    Train_Dataset = JointDataset(X_train,y_train)
    Test_Dataset = JointDataset(X_test, y_test)

    Train_DL = DataLoader(dataset=Train_Dataset,batch_size=batch_size,drop_last=drop_last,shuffle=shuffle)
    Test_DL = DataLoader(dataset=Test_Dataset, batch_size=batch_size, drop_last=drop_last,shuffle=shuffle)

    #X_train_DL= DataLoader(X_train,batch_size=batch_size,drop_last=drop_last)
    #y_train_DL = DataLoader(y_train,batch_size=batch_size,drop_last=drop_last)
    #X_test_DL = DataLoader(X_test,batch_size=batch_size,drop_last=drop_last)
    #y_test_DL = DataLoader(y_test,batch_size=batch_size,drop_last=drop_last)

    return Train_DL, Test_DL

class JointDataset(Dataset):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __len__(self):
        return len(self.x)
    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]
def DF_to_TSDataSet_PF(df_train,df_val, max_encoder_length = 60, max_prediction_length = 20):
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
