import os
from ENGINE.DATA_API import OandaData
from ENGINE.DATA_API import FXCMData

current_path = os.getcwd()

FD = FXCMData('C:\\Users\\aleksander\\PycharmProjects\\FXCM\\')
OD = OandaData('C:\\Users\\aleksander\\PycharmProjects\\OANDA\\')
pair = "EUR_USD"
tf = "H1"
data = OD.GetData("2002-01-01T00:00:00Z", "2021-04-21T00:00:00Z", pair, tf, "DF")
