from abc import ABC, abstractmethod
import os

class Transaction(ABC):

    def __init__(self, data):
        self.ticket = 0
        self.price = 0.0
        self.time = ""
        self.symbol = ""
        self.size = 0.0

    @abstractmethod
    def do_something(self):
        pass


class TransactionMT4(Transaction):
    def __init__(self,data):
        self.ticket = data["ticket"]
        self.price = data["price"]
        self.time = data["time"]
        self.symbol = data["symbol"]
        self.size = data["size"]

    def do_something(self):
        pass

class TransactionCTRADER(Transaction):
    def __init__(self,data):
        self.ticket = data["ticket"]
        self.price = data["price"]
        self.time = data["time"]
        self.symbol = data["symbol"]
        self.size = data["size"]

    def do_something(self):
        pass