import pandas as pd
from neuralforecast import NeuralForecast
from neuralforecast.models import TFT
import torch

# Set the device to the first GPU
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Load your OHLC dataset (assumed to be in a pandas DataFrame format)
# The dataset must contain: unique_id (series identifier), ds (timestamp), O, H, L, C columns (Open, High, Low, Close).
df = pd.read_csv('EURUSD_60M.csv')

# Prepare the data for the NeuralForecast model
df = df.rename(columns={'C': 'y'})  # Rename the Close price as 'y', which will be our target variable
df = df.rename(columns={'Time': 'ds'})
df['unique_id'] = 'series_1'
df['ds'] = pd.to_datetime(df['ds'], errors='coerce')


# Initialize the TFT model for hourly data
tft = TFT(input_size=24,  # Number of historical steps (1 week of hourly data = 24 hours * 7 days)
          h=1,             # Forecast horizon (predict the next 24 hours)
          hidden_size=64,    # Size of hidden layers
          dropout=0.1,       # Dropout rate for regularization
          learning_rate=1e-3)

# Define the forecasting model with the TFT and other settings
model = NeuralForecast(models=[tft],
                       freq='H')

# Fit the model (NeuralForecast handles the dataset preparation)
model.fit(df)

# Forecast the next 24 periods (hours) for each unique series
forecasts_df = model.predict()

# Display the forecast results
print(forecasts_df.head())

# Optionally, you can save the forecasts
forecasts_df.to_csv('tft_forecasts_hourly.csv', index=False)



