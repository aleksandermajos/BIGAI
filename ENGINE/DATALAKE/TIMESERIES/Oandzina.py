from Oanda_Data import OandaData
OD = OandaData()
data = OD.GetData("2021-01-01T00:00:00Z", "2021-04-21T00:00:00Z", "EUR_USD", "M15", "DF")

oko = 4