from abc import ABC, abstractmethod
from ENGINE.AI.DL.TIMESERIES.transaction import TransactionMT4
import os
import subprocess

class Account(ABC):

    def __init__(self, data):
        self.signal_speed_to_broker = list()
        self.signal_speed_from_broker = list()
        self.signal_speed_tranzaction_in = list()
        self.signal_speed_tranzaction_out = list()
        super(Account, self).__init__()

    @abstractmethod
    def do_something(self):
        pass


class AccountCTRADER(Account):
    def __init__(self,data):
        self.server_name_external = data["server"]
        self.ip_adress = ''
        self.signal_speed_from_broker,self.ip_adress = AccountCTRADER.find_signal_speed_to_broker(self.server_name_external)
        self.transactions = list()
        self.closed_transactions = list()
        self.deposit_currency = data["currency"]
        self.balance = data["balance"]
        self.equity = data["equity"]
        self.margin = data["margin"]

    def find_signal_speed_to_broker(server_name):
        out = subprocess.run(['ping', server_name], capture_output=True)
        str = out.stdout.decode("utf-8")
        start_ip = str.find('[')
        stop_ip = str.find(']')
        ip_adress = str[start_ip+1:stop_ip]
        start_maximum = str.find("Maximum")
        stop_maximum = str.find("Average")
        max = str[start_maximum+10:stop_maximum-4]
        max = int(max)
        return max, ip_adress


    def do_something(self):
        pass


class AccountMT4(Account):
    def __init__(self,data):
        self.server_name_internal = data["server"]
        self.ip_adress = ''
        self.server_name_external = AccountMT4.find_dns_name(self.server_name_internal)
        self.signal_speed_from_broker,self.ip_adress = AccountMT4.find_signal_speed_to_broker(self.server_name_external)
        self.transactions = list()
        self.closed_transactions = list()
        self.deposit_currency = ""
        self.balance = 0
        self.equity = 0
        self.margin = 0

    def find_dns_name(internal_name):
        if internal_name == "OANDA-v20 Live-2": return "mt4-ng-trade02.oanda.com"
        if internal_name == "MetaQuotes-Demo": return "access.metatrader5.com"
        if internal_name == "FxPro-MT5": return "access.metatrader5.com"
        if internal_name == "BICMarkets-Demo": return "access.metatrader5.com"
        if internal_name == "XTrade-Real3": return "real3a.xtb.com"
        if internal_name == "XtradeServer-MT4 Demo": return "demoa.xtb.com"
        if internal_name == "XtradeServer-Real": return "real1a.xtb.com"
        if internal_name == "XtradeServer-Real2": return "real2a.xtb.com"
        if internal_name == "XtradeServer-Real3": return "real3a.xtb.com"
        else: return ""

    def find_signal_speed_to_broker(server_name):

        out = subprocess.run(['ping', server_name], capture_output=True)
        str = out.stdout.decode("utf-8")
        start_ip = str.find('[')
        stop_ip = str.find(']')
        ip_adress = str[start_ip+1:stop_ip]
        start_maximum = str.find("Maximum")
        stop_maximum = str.find("Average")
        max = str[start_maximum+10:stop_maximum-4]
        max = int(max)

        return max, ip_adress


    def do_something(self):
        pass

class AccountFXCMAPI(Account):
    def __init__(self,server_name):
        self.server_name = server_name
        self.ip_adress = ''
        self.signal_speed_from_broker,self.ip_adress = AccountFXCMAPI.find_signal_speed_to_broker(self.server_name)

    def find_signal_speed_to_broker(server_name):
        out = subprocess.run(['ping', server_name], capture_output=True)
        str = out.stdout.decode("utf-8")
        start_ip = str.find('[')
        stop_ip = str.find(']')
        ip_adress = str[start_ip+1:stop_ip]
        start_maximum = str.find("Maximum")
        stop_maximum = str.find("Average")
        max = str[start_maximum+10:stop_maximum-4]
        max = int(max)
        return max, ip_adress


    def do_something(self):
        pass

class AccountFIX(Account):
    def __init__(self,server_data,server_trade):
        self.server_data = server_data
        self.server_trade = server_trade
        self.ip_adress_data = ''
        self.ip_adress_trade = ''
        self.signal_speed_from_broker_data,self.ip_adress_data = AccountFIX.find_signal_speed_to_broker(self.server_data)

    def find_signal_speed_to_broker(server_name):
        out = subprocess.run(['ping', server_name], capture_output=True)
        str = out.stdout.decode("utf-8")
        start_ip = str.find('[')
        stop_ip = str.find(']')
        ip_adress = str[start_ip+1:stop_ip]
        start_maximum = str.find("Maximum")
        stop_maximum = str.find("Average")
        max = str[start_maximum+10:stop_maximum-4]
        max = int(max)
        return max, ip_adress


    def do_something(self):
        pass