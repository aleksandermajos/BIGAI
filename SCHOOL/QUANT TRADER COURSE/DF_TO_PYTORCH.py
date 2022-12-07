from ENGINE.DATA_DF_TO_PYTORCH import DF_TO_PYTORCH
from ENGINE.DATA_DF_TO_PYTORCH import DF_TO_PYTORCH_DATASET
from ENGINE.DATA_PLAT_CLASSIFICATION_QM import MT4_CSV_TO_CLASSIFICATION
from os import fspath
from pathlib import Path


data_path = Path(Path(__file__).resolve().parent)
data_path_last = fspath(data_path)

data_MT4 = data_path_last+"\\DATA\\QM_MT4_CSV/EURUSD.30.csv"
X,Y = MT4_CSV_TO_CLASSIFICATION(data_MT4, 16)
X_train, y_train, X_test, y_test = DF_TO_PYTORCH(X,Y,0.33,scaler=True)
Train_DL, Test_DL = DF_TO_PYTORCH_DATASET(X,Y,0.33,scaler=True,batch_size=25,drop_last=False,shuffle=True)
for i,batch in enumerate(Train_DL,1):
    for j in batch:
        print(j)
