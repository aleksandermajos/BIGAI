import pandas as pd
from neuralforecast import NeuralForecast
from neuralforecast.models import TFT
import torch
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
from sklearn.model_selection import train_test_split


df = pd.read_csv('EURUSD_60M.csv')

df['y'] = df['C']
df['y'] = df['y'].shift(-1).fillna(0)
df = df.rename(columns={'Time': 'ds'})
df['unique_id'] = 'series_1'
df['ds'] = pd.to_datetime(df['ds'], errors='coerce')
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)


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
model.fit(train_df)

test_forecast = model.predict(test_df)

# Assuming your test_df contains the actual values in column 'y'
# Compare predictions with actual values
comparison_df = test_df[['ds', 'y']].copy()  # Copy actual values
comparison_df['y_hat'] = test_forecast['y_hat']  # Add predictions

# Display the comparison
print(comparison_df.head())

# Optionally calculate some metrics
from sklearn.metrics import mean_squared_error, mean_absolute_error

mse = mean_squared_error(comparison_df['y'], comparison_df['y_hat'])
mae = mean_absolute_error(comparison_df['y'], comparison_df['y_hat'])



