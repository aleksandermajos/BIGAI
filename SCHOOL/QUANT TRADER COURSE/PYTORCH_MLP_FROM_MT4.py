from ENGINE.DATA_DF_TO_PYTORCH import DF_TO_PYTORCH
from BUSINESS.QUANT.DATA_PLAT_CLASSIFICATION_QM import MT4_CSV_TO_CLASSIFICATION
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F
import torch.nn as nn
import tqdm

from os import fspath
from pathlib import Path

data_path = Path(Path(__file__).resolve().parent)
data_path_last = fspath(data_path)

data_MT4 = data_path_last+"\\DATA\\QM_MT4_CSV/EURUSD.30.csv"
X,Y = MT4_CSV_TO_CLASSIFICATION(data_MT4, 16)
X_train, y_train, X_test, y_test = DF_TO_PYTORCH(X,Y,0.33,scaler=True)

class Model(nn.Module):
    def __init__(self, input_dim):
        super(Model, self).__init__()
        self.layer1 = nn.Linear(input_dim, 2*input_dim)
        self.layer2 = nn.Linear(2*input_dim, 2*input_dim)
        self.layer3 = nn.Linear(2*input_dim, 1)

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        x = F.sigmoid(self.layer3(x))
        return x

model = Model(X_train.shape[1])
optimizer = torch.optim.SGD(model.parameters(), lr=0.001)
loss_fn = nn.BCEWithLogitsLoss()

EPOCHS = 1000


loss_list = np.zeros((EPOCHS,))
accuracy_list = np.zeros((EPOCHS,))


for epoch in tqdm.trange(EPOCHS):
    print(epoch)
    y_pred = model(X_train)
    loss = loss_fn(y_pred, y_train)
    loss_list[epoch] = loss.item()

    # Zero gradients
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    with torch.no_grad():
        y_pred = model(X_test)
        correct = (torch.argmax(y_pred, dim=1) == y_test).type(torch.FloatTensor)
        accuracy_list[epoch] = correct.mean()


fig, (ax1, ax2) = plt.subplots(2, figsize=(12, 6), sharex=True)
ax1.plot(accuracy_list)
ax1.set_ylabel("validation accuracy")
ax2.plot(loss_list)
ax2.set_ylabel("validation loss")
ax2.set_xlabel("epochs")
plt.show()

from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import OneHotEncoder

plt.figure(figsize=(10, 10))
plt.plot([0, 1], [0, 1], 'k--')

# One hot encoding
enc = OneHotEncoder()
Y_onehot = enc.fit_transform(y_test[:, np.newaxis]).toarray()

with torch.no_grad():
    y_pred = model(X_test).numpy()
    fpr, tpr, threshold = roc_curve(Y_onehot.ravel(), y_pred.ravel())

plt.plot(fpr, tpr, label='AUC = {:.3f}'.format(auc(fpr, tpr)))
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.title('ROC curve')
plt.legend()
plt.show()
oko=5


