from abc import ABC, abstractmethod
from ENGINE.QM_INSTRUMENT import InstrumentMT4, InstrumentCTRADER
from ENGINE.QM_ACCOUNT import AccountMT4, AccountCTRADER, AccountFXCMAPI, AccountFIX
from ENGINE.QM_TRANSACTION import TransactionMT4, TransactionCTRADER
from ENGINE.QM_DATA_API import exampleAuth_OANDA, exampleAuth_FXCM, FXCMData
from ENGINE.QM_TIME_OPENING_CLOSING_MT4 import Open_Time_To_New_Chart, Close_Time_To_New_Chart
from ENGINE.QM_TIME_OPENING_CLOSING_MT4 import Average_OpenTimes, Average_CloseTimes
import json
import pandas as pd
import zmq
import zmq.asyncio
import socket
from datetime import datetime
import functools
import oandapyV20.endpoints.pricing as pricing
import oandapyV20
import fxcmpy
import time
import numpy as np
import os

from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/BIGAI/'
path = path_beginning+"DATA/QUANTMAVERICK/"


class Chart(ABC):

    def __init__(self, data):
        self.WindowID = ""
        super(Chart, self).__init__()

    @abstractmethod
    def GetData(self):
        pass

class ChartFX(Chart):
    def __init__(self, data,subport,reqport):
        self.Terminal = data["Terminal"]
        self.Broker = data["Broker"]
        self.Symbol = data["Symbol"]
        self.Period = data["Period"]
        self.WindowID = data["WindowID"]
        #data_path = Path(Path(__file__).resolve().parent.parent)
        #data_path_last = fspath(data_path)
        self.broker_open_times = path+"BROKERS_OPEN_TIMES.csv"
        self.OpenTimes = Open_Time_To_New_Chart(self,self.broker_open_times)
        self.Average_OpenTimes = Average_OpenTimes(self)
        self.broker_close_times = path+"BROKERS_CLOSE_TIMES.csv"
        self.ClosingTimes = Close_Time_To_New_Chart(self,self.broker_close_times)
        self.Average_CloseTimes = Average_CloseTimes(self)
        self.subport = subport
        self.reqport = reqport
        self.context = zmq.Context()
        self.sub = self.context.socket(zmq.SUB)
        self.req = self.context.socket(zmq.REQ)
        self.sub.connect("tcp://localhost:" + self.subport)
        self.sub.subscribe("")
        self.req.connect("tcp://localhost:" + self.reqport)
        self.data_candles_path = path+"DATA_CANDLES.csv"
        self.req.send(b"INSTRUMENTINFO")
        data = self.req.recv()
        data = data.decode('utf8').replace("}{", ", ")
        my_json = json.loads(data)
        json.dumps(data, indent=4, sort_keys=True)
        if self.Terminal == "MT4" or self.Terminal == "MT5":  self.instrument = InstrumentMT4(my_json)
        if self.Terminal == "CTRADER" :  self.instrument = InstrumentCTRADER(my_json)
        self.req.send(b"HISTORY")
        data = self.req.recv()
        if len(data) > 2:
            data = data.decode('utf8')
            print(os.getcwd())
            data_path_last = path+"DATA_CANDLES.csv"
            self.data_candles_path = data_path_last
            f = open(data_path_last, "w")
            f.write(data[:])
            f.close()
            file = open(data_path_last, "r")
            self.history = pd.read_csv(file)
        self.tick = ''
        self.req.send(b"ACCOUNTINFO")
        data = self.req.recv()
        data = data.decode('utf8').replace("}{", ", ")
        my_json = json.loads(data)
        json.dumps(data, indent=4, sort_keys=True)
        if self.Terminal == "MT4" or self.Terminal == "MT5": self.account = AccountMT4(my_json)
        if self.Terminal == "CTRADER" :  self.account = AccountCTRADER(my_json)

        self.req.send(b"TRANSACTIONS")
        data = self.req.recv()
        if len(data) > 2:
            data = data.decode('utf8').replace("}{", "}}{{")
            x = data.split("}{")
            for i in range(len(x)):
                my_json = json.loads(x[i])
                json.dumps(i, indent=4, sort_keys=True)
                if self.Terminal == "MT4" or self.Terminal == "MT5": self.account.transactions.append(TransactionMT4(my_json))
                if self.Terminal == "CTRADER":  self.account.transactions.append(TransactionCTRADER(my_json))

        self.RecentTicks = pd.DataFrame()
        self.actuall = pd.DataFrame()
        self.previous = pd.DataFrame()
        self.Bid_diff = 0
        self.Ask_diff = 0


        oko=5

    def GetData(self,data):
        s = pd.Series({'Bid':data["bid"], 'Ask': data["ask"]})
        data["time"] = np.datetime64(data["time"])
        df = pd.DataFrame([s], index=[data["time"]])
        df = df.reset_index(drop=False)
        df.rename(columns={'index': 'Terminal Time'}, inplace=True)
        terminal_time = df.iloc[0,0]
        creation_time = terminal_time - np.timedelta64(self.account.signal_speed_from_broker, 'ms')
        current_time = pd.Timestamp.utcnow().replace(tzinfo=None)
        df.insert(0,"Creation Time",creation_time)
        df.insert(2, "Current Time", current_time)
        creation_terminal_delta = terminal_time - creation_time
        current_terminal_dalta = current_time - terminal_time
        creation_current_delta = current_time - creation_time
        df.insert(3, 'Creation-Terminal Time', creation_terminal_delta.delta/1000000)
        df.insert(4, 'Terminal-Current Time', current_terminal_dalta.delta/1000000)
        df.insert(5, 'Creation-Current Time', creation_current_delta.delta/1000000)
        if "X-Trade Brokers DM SA" in data["Broker"] or "OANDA DIVISION1" in data["Broker"] \
                or "MetaQuotes Software Corp." in data["Broker"] or "Dom Maklerski Banku Ochrony Srodowiska S.A." in data["Broker"]\
                or "Dom Maklerski mBanku" in data["Broker"] or "B.I.C. Markets Co., Ltd." in data["Broker"]\
                or "FXPRO Financial Services Ltd" in data["Broker"]:
            df["TypeBroker"] = "MM"
        if data["Broker"] == "FXPRO":
            df["TypeBroker"] = "ECN"
        df["BrokerName"] = data["Broker"]
        if "X-Trade Brokers DM SA" in data["Broker"] or "OANDA DIVISION1" in data["Broker"]:
            df["DR"] = "REAL"
        if "MetaQuotes Software Corp." in data["Broker"] or "Dom Maklerski Banku Ochrony Srodowiska S.A." in data["Broker"]\
                or "Dom Maklerski mBanku" in data["Broker"] or "FXPRO Financial Services Ltd" in data["Broker"]\
                or "B.I.C. Markets Co., Ltd." in data["Broker"] or "FXPRO" in data["Broker"]:
            df["DR"] = "DEMO"
        df["Terminal"] = data["Terminal"]
        df["Protocol"] = "ZMQ"
        df["Period"] = data["Period"]
        df["Symbol"] = data["Symbol"]
        df["Ask_Diff"] = 0.0
        df["Bid_Diff"] = 0.0
        df["UP"] = 0
        df["Spread"] = self.instrument.spread
        df["OpeningTime"] = self.Average_OpenTimes
        df["ClosingTime"] = self.Average_CloseTimes
        if self.RecentTicks.empty:
            self.RecentTicks = df
        else:
            self.RecentTicks = pd.concat([self.RecentTicks, df])
            if self.RecentTicks.shape[0] > 1:
                self.actuall = self.RecentTicks.iloc[-1:]
                self.previous = self.RecentTicks.iloc[-2:-1]
                self.Bid_diff = self.actuall["Bid"].iloc[0]-self.previous["Bid"].iloc[0]
                self.Ask_diff = self.actuall["Ask"].iloc[0] - self.previous["Ask"].iloc[0]
                df["Ask_Diff"] = self.Ask_diff
                df["Bid_Diff"] = self.Bid_diff
        if self.Ask_diff >0 and self.Bid_diff > 0:
            df["UP"] = 1
        if self.Ask_diff < 0 and self.Bid_diff < 0:
            df["UP"] = -1
        return df


class ChartOanda(Chart):
    def __init__(self, Symbol):
        self.Broker = "Oanda"
        self.Symbol = Symbol
        self.oanda_accountID, self.oanda_access_token = exampleAuth_OANDA("/Users/aleksander/PycharmProjects/OANDA/")
        self.oanda_client = oandapyV20.API(access_token=self.oanda_access_token, environment="practice")
        self.params = {"instruments": "EUR_USD"}
        self.oanda_r = pricing.PricingInfo(accountID=self.oanda_accountID, params=self.params)
        self.tick = ""

    def GetData(self):
        rv = self.oanda_client.request(self.oanda_r)
        self.tick=self.oanda_r.response
        return self.tick

class ChartFXCM(Chart):
    def __init__(self):
        self.token = exampleAuth_FXCM('/Users/aleksander/PycharmProjects/FXCM/')
        self.fxcm_con = fxcmpy.fxcmpy(access_token=self.token, log_level='error')
        self.server_name = "api-demo.fxcm.com"
        self.Broker = "FXCM"







    def GetData(self,Symbol):
        self.tick = self.fxcm_con.get_last_price(Symbol)
        df = pd.DataFrame([self.tick])
        df = df.reset_index(drop=False)
        df.rename(columns={'index': 'Creation Time'}, inplace=True)
        df = df.drop("Low", axis=1)
        df = df.drop("High", axis=1)
        creation_time = df.iloc[0, 0]
        terminal_time = creation_time
        current_time = pd.Timestamp.utcnow().replace(tzinfo=None)
        df.insert(1, "Terminal Time", terminal_time)
        df.insert(2, "Current Time", current_time)
        creation_terminal_delta = terminal_time - creation_time
        current_terminal_dalta = current_time - terminal_time
        creation_current_delta = current_time - creation_time
        df.insert(3, 'X', creation_terminal_delta.delta / 1000000)
        df.insert(4, 'Y', current_terminal_dalta.delta / 1000000)
        df.insert(5, 'Z', creation_current_delta.delta / 1000000)
        df['TypeBroker'] = "MM"
        df["BrokerName"] = "FXCM"
        df["DR"] = "DEMO"
        df["Terminal"] = "None"
        df["Protocol"] = "RESTAPI"
        df["Symbol"] = Symbol
        self.tick = df
        return df


class ChartFIX(Chart):
    def __init__(self, Symbol):
        self.Broker = "FXPRO"
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.s.connect(("h20.p.ctrader.com", 5201))
        self.headerAndBodyAndTrailer = self.LogonPacket()
        print('LOGON packet sent to ctrader!!!')
        self.s.sendall(self.headerAndBodyAndTrailer.encode(encoding='ascii'))
        self.data = self.s.recv(1024)
        self.data = str(self.data)
        print('\n\nLOGON RESP :  ', self.data)
        self.subscription_id = 876316403
        self.seq_num = 2
        self.headerAndBodyAndTrailer = ChartFIX.MarketDataReq(self, str(self.seq_num), str(self.subscription_id))
        print('MARTKET_DATA_REQ packet sent to ctrader!!!')
        self.s.sendall(self.headerAndBodyAndTrailer.encode(encoding='ascii'))
        self.data = self.s.recv(1024)
        print(self.data)
        self.tick = ''
        self.account = AccountFIX("h20.p.ctrader.com","h20.p.ctrader.com")

    def GetData(self,Symbol):
        start = time.time_ns()
        self.seq_num += 1
        data = self.s.recv(1024)
        data = str(data)
        stop = time.time_ns()
        diff = stop-start
        if data == 'b\'\'':
            return pd.DataFrame()
        if "USE" in data:
            headerAndBodyAndTrailer = self.MarketDataReq(str(self.seq_num), str(self.subscription_id))
            print('MARTKET_DATA_REQ packet sent to ctrader!!!')
            self.s.sendall(headerAndBodyAndTrailer.encode(encoding='ascii'))
            self.seq_num += 1
        data = self.s.recv(1024)
        data = str(data)
        if data != 'b\'\'':
            t, bid, ask = ChartFIX.retreive_info(self, data)
            if t==0:
                return pd.DataFrame()
            s = pd.Series({'Bid': bid,'Ask': ask})
            df = pd.DataFrame([s],index=[t])
            df = df.reset_index(drop=False)
            df.rename(columns={'index': 'Creation Time'}, inplace=True)
            creation_time = df.iloc[0, 0]
            terminal_time = creation_time
            current_time = pd.Timestamp.utcnow().replace(tzinfo=None)
            df.insert(1, "Terminal Time", terminal_time)
            df.insert(2, "Current Time", current_time)
            creation_terminal_delta = terminal_time - creation_time
            current_terminal_dalta = current_time - terminal_time
            creation_current_delta = current_time - creation_time
            df.insert(3, 'X', creation_terminal_delta.delta / 1000000)
            df.insert(4, 'Y', current_terminal_dalta.delta / 1000000)
            df.insert(5, 'Z', creation_current_delta.delta / 1000000)
            df['TypeBroker'] = "ECN"
            df["BrokerName"] = "FXPRO"
            df["DR"] = "DEMO"
            df["Terminal"] = "cTrader"
            df["Protocol"] = "FIX"
            df["Symbol"] = Symbol
            self.tick = df
            return df

    def retreive_info(self,str):
        start_data_index = str.find('x0152=')
        if start_data_index == -1:
            return 0,0,0
        stop_data_index = str.find('x0156=')
        data = str[start_data_index + 6:stop_data_index - 1]
        data = data[0:4]+'-'+data[4:6]+'-'+data[6:8]+ ' ' +data[9:]
        data = np.datetime64(data)

        start_bid_index = str.find('x01269=0\\x01270=')
        stop_bid_index = str.find('x01269=1')
        bid = str[start_bid_index + 16:stop_bid_index - 1]

        start_ask_index = str.find('x01269=1\\x01270=')
        stop_ask_index = str.find('x0110=')
        ask = str[start_ask_index + 16:stop_ask_index - 1]
        return data, bid, ask

    def ConstructHeader(msg_type, SenderCompID, TargetCompID, SenderSubID, TargetSubID, messageSequenceNumber):
        header = ''
        header += "8=FIX.4.4|"
        message = ''
        message += "35=" + msg_type + "|"
        message += "49=" + SenderCompID + "|"
        message += "56=" + TargetCompID + "|"
        message += "50=" + SenderSubID + "|"
        message += "57=" + TargetSubID + "|"
        message += "34=" + messageSequenceNumber + "|"
        utctimenow_year = str(datetime.utcnow().year)
        utctimenow_month = str(datetime.utcnow().month)
        if len(utctimenow_month) == 1: utctimenow_month = '0' + utctimenow_month
        utctimenow_date = str(datetime.utcnow().day)
        utctimenow_date = utctimenow_date.zfill(2)
        utctimenow_hour = str(datetime.utcnow().hour)
        utctimenow_hour = utctimenow_hour.zfill(2)
        utctimenow_min = str(datetime.utcnow().minute)
        utctimenow_min = utctimenow_min.zfill(2)
        utctime = utctimenow_year + utctimenow_month + utctimenow_date + '-' + utctimenow_hour + ':' + utctimenow_min + ':00'
        message += "52=" + utctime + "|"
        return header, message

    def ConstructTrailer(headerAndBody):
        headerAndBody = str(headerAndBody.replace('|', chr(0x01)))
        chksum = str(functools.reduce(lambda x, y: x + y, map(ord, headerAndBody)) % 256)
        chksum = chksum.zfill(3)
        return chksum

    def LogonMessage(heartBeatSeconds, username, password, resetSeqNum):
        body = ''
        # Encryption
        body += "98=0|"
        body += "108=" + heartBeatSeconds + "|"
        if resetSeqNum:
            body += "141=Y|"
        body += "553=" + username + "|"
        body += "554=" + password + "|"
        return body

    def LogonPacket(self):
        # Header
        msg_type = 'A'
        SenderCompID = 'fxpro.10268378'
        TargetCompID = 'CSERVER'
        SenderSubID = 'any_string'
        TargetSubID = 'QUOTE'
        messageSequenceNumber = '1'
        header, message = ChartFIX.ConstructHeader(msg_type, SenderCompID, TargetCompID, SenderSubID, TargetSubID, messageSequenceNumber)
        # Body
        heartBeatSeconds = '30'
        username = '10268378'
        password = 'forexklon666'
        resetSeqNum = 1
        body = ChartFIX.LogonMessage(heartBeatSeconds, username, password, resetSeqNum)
        length = len(message) + len(body)
        header += "9=" + str(length) + "|"
        header = header + message
        print('Header construction completed')
        print('Header is: ', header, '\n')
        headerAndBody = header + body
        # Trailer
        chksum = ChartFIX.ConstructTrailer(headerAndBody)
        trailer = "10=" + str(chksum) + "|"
        print('Trailer construction completed')
        print('Trailer is: ', trailer, '\n')
        headerAndBodyAndTrailer = headerAndBody + trailer
        print('ctrader packet is: ', headerAndBodyAndTrailer, '\n')
        headerAndBodyAndTrailer = headerAndBodyAndTrailer.replace("|", chr(0x01))
        return headerAndBodyAndTrailer

    def MarketDataReq(self, seq_num, subscription_id):
        # Header
        msg_type = 'V'
        SenderCompID = 'fxpro.10268378'
        TargetCompID = 'CSERVER'
        SenderSubID = 'any_string'
        TargetSubID = 'QUOTE'
        messageSequenceNumber = seq_num
        header, message = ChartFIX.ConstructHeader(msg_type, SenderCompID, TargetCompID, SenderSubID, TargetSubID, messageSequenceNumber)
        # Body
        body = "262=" + subscription_id + "|263=1|264=1|265=1|146=1|55=1|267=2|269=0|269=1|"
        length = len(message) + len(body)
        header += "9=" + str(length) + "|"
        header = header + message
        headerAndBody = header + body
        chksum = ChartFIX.ConstructTrailer(headerAndBody)
        trailer = "10=" + str(chksum) + "|"
        headerAndBodyAndTrailer = headerAndBody + trailer
        headerAndBodyAndTrailer = headerAndBodyAndTrailer.replace("|", chr(0x01))
        return headerAndBodyAndTrailer

    def MarketDataIncrementalRefresh(self,seq_num, subscription_id):
        # Header
        msg_type = 'X'
        SenderCompID = 'fxpro.10268378'
        TargetCompID = 'CSERVER'
        SenderSubID = 'any_string'
        TargetSubID = 'QUOTE'
        messageSequenceNumber = seq_num
        header, message = self.ConstructHeader(msg_type, SenderCompID, TargetCompID, SenderSubID, TargetSubID,
                                          messageSequenceNumber)
        body = "262=" + subscription_id + "|263=1|264=1|269=0|268=2|279=0|55=1|58=1|270=0|"
        length = len(message) + len(body)
        header += "9=" + str(length) + "|"
        header = header + message
        headerAndBody = header + body

        # Trailer
        chksum = self.ConstructTrailer(headerAndBody)
        trailer = "10=" + str(chksum) + "|"
        headerAndBodyAndTrailer = headerAndBody + trailer
        headerAndBodyAndTrailer = headerAndBodyAndTrailer.replace("|", chr(0x01))
        return headerAndBodyAndTrailer