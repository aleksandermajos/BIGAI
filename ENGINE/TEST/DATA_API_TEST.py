import os
import platform
from ENGINE.DATA_API import OandaData
from ENGINE.DATA_API import FXCMData

current_path = os.getcwd()
op_sys = platform.uname()


if op_sys.system == 'Windows':
    FD = FXCMData('C:\\Users\\aleksander\\PycharmProjects\\FXCM\\')
    OD = OandaData('C:\\Users\\aleksander\\PycharmProjects\\OANDA\\')
if op_sys.system =='MAC':
    FD = FXCMData('/Users/aleksander/PycharmProjects/FXCM/')
    OD = OandaData('/Users/aleksander/PycharmProjects/OANDA/')

pair = "EUR_USD"
tf = "H1"
data = OD.GetData("2002-01-01T00:00:00Z", "2021-04-21T00:00:00Z", pair, tf, "DF")
oko=5