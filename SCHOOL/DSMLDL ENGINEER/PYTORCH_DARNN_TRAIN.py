import torch
from torch import nn
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
import sys, os


def Train_DARNN(model,data_prepared, epochs, model_save_name):
    opt = torch.optim.Adam(model.parameters(), lr=0.001)
    epoch_scheduler = torch.optim.lr_scheduler.StepLR(opt, 20, gamma=0.9)
    epochs = epochs
    loss = nn.MSELoss()
    patience = 15
    min_val_loss = 9999
    counter = 0
    for i in range(epochs):
        mse_train = 0
        for batch_x, batch_y_h, batch_y in data_prepared['data_train_loader']:
            batch_x = batch_x.cuda()
            batch_y = batch_y.cuda()
            batch_y_h = batch_y_h.cuda()
            opt.zero_grad()
            y_pred = model(batch_x, batch_y_h)
            y_pred = y_pred.squeeze(1)
            l = loss(y_pred, batch_y)
            l.backward()
            mse_train += l.item() * batch_x.shape[0]
            opt.step()
        epoch_scheduler.step()
        with torch.no_grad():
            mse_val = 0
            preds = []
            true = []
            for batch_x, batch_y_h, batch_y in data_prepared['data_val_loader']:
                batch_x = batch_x.cuda()
                batch_y = batch_y.cuda()
                batch_y_h = batch_y_h.cuda()
                output = model(batch_x, batch_y_h)
                output = output.squeeze(1)
                preds.append(output.detach().cpu().numpy())
                true.append(batch_y.detach().cpu().numpy())
                mse_val += loss(output, batch_y).item() * batch_x.shape[0]
        preds = np.concatenate(preds)
        true = np.concatenate(true)

        if min_val_loss > mse_val ** 0.5:
            min_val_loss = mse_val ** 0.5
            print("Saving...")
            file_dir = os.path.dirname(__file__)
            path_to_save = file_dir+"\\TRAINED\\PREDICTORS\\"+model_save_name
            torch.save(model.state_dict(), path_to_save)
            counter = 0
        else:
            counter += 1

        if counter == patience:
            break
        print("Iter: ", i, "train: ", (mse_train / len(data_prepared['X_train_t'])) ** 0.5, "val: ", (mse_val / len(data_prepared['X_val_t'])) ** 0.5)
        if (i % 10 == 0):
            preds = preds * (data_prepared['target_train_max'] - data_prepared['target_train_min']) + data_prepared['target_train_min']
            true = true * (data_prepared['target_train_max'] - data_prepared['target_train_min']) + data_prepared['target_train_min']
            mse = mean_squared_error(true, preds)
            mae = mean_absolute_error(true, preds)
            print("mse: ", mse, "mae: ", mae)