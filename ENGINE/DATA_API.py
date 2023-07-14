from ENGINE.DATA_OHLC_MANIPULATE import Add_Growing_Column, Add_Diff_CO_Column, List_Of_Dict_To_DF
from pathlib import Path
from os import fspath
import oandapyV20
from oandapyV20.contrib.factories import InstrumentsCandlesFactory
import fxcmpy


def exampleAuth_OANDA(path):
    accountID, token = None, None
    with open(path + "account.txt") as I:
        accountID = I.read().strip()
    with open(path + "token.txt") as I:
        token = I.read().strip()
    return accountID, token

def exampleAuth_FXCM(path):
    token = None
    with open(path + "token.txt") as I:
        token = I.read().strip()
    return token


class OandaData():
    def __init__(self,path):
        self.accountID, self.token = exampleAuth_OANDA(path)

    def GetData(self,start, stop, instrument, period, format):
        self.start = start
        self.stop = stop
        self.instrument = instrument
        self.period = period
        self.format = format
        return self.get_history_oanda(self.accountID,self.token,self.start,self.stop ,self.instrument,self.period,self.format)

    def GenerateData(self,path_file):
        pairs = ["EUR_USD", "USD_JPY", "GBP_USD", "USD_CAD", "USD_CHF", "AUD_USD"]
        tf = ["M15", "M30", "H1", "H4", "H12"]
        for pair in pairs:
            for timeframe in tf:
                data_df = self.GetData("2002-01-01T00:00:00Z", "2021-04-21T00:00:00Z", pair, timeframe, "DF")
                path = path_file + pair + "_" + timeframe + ".csv"
                data_path = Path(Path(__file__).resolve().parent.parent.parent) / path
                data_path_last = fspath(data_path)
                data_df = Add_Diff_CO_Column(data_df)
                data_df = Add_Growing_Column(data_df)
                data_df.to_csv(data_path_last, index=False)

    def get_history_oanda(self,accountID, token, start, stop, instrument, granularity, format):

        client = oandapyV20.API(token, environment="practice")

        params = {
            "from": start,
            "to": stop,
            "granularity": granularity,
            "count": 4500
        }

        lista = []
        for r in InstrumentsCandlesFactory(instrument=instrument, params=params):
            client.request(r)
            lista.append(r.response.get('candles'))

        if format == "DF": return List_Of_Dict_To_DF(lista)

class FXCMData():
    def __init__(self,path):
        self.token = exampleAuth_FXCM(path)
        self.fxcm_con = fxcmpy.fxcmpy(access_token=self.token, log_level='error')
        self.server_name = "api-demo.fxcm.com"
        self.Broker = "FXCM"



    def GetData(self,start, stop, instrument, period, format):
        self.start = start
        self.stop = stop
        self.instrument = instrument
        self.period = period
        self.format = format
        self.fxcm_con.subscribe_market_data(self.instrument)
        self.tick = ""









