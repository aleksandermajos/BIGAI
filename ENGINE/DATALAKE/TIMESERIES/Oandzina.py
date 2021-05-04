from Oanda_Data import OandaData
from ENGINE.DATALAKE.TIMESERIES.OHLC_Manipulate import OHLC_DF_to_REGRESSION_C, OHLC_DF_to_CLASSIFICATION_C
OD = OandaData()
data = OD.GetData("2021-01-01T00:00:00Z", "2021-04-21T00:00:00Z", "EUR_USD", "M15", "DF")
df = OHLC_DF_to_CLASSIFICATION_C(data)
oko = 4