from abc import ABC, abstractmethod

class Instrument(ABC):

    def __init__(self, data):
        super(Instrument, self).__init__()

    @abstractmethod
    def do_something(self):
        pass

class InstrumentCTRADER(Instrument):
    def __init__(self,data):
        self.name = data["symbol"]
        self.points = data["points"]
        self.digits = data["digits"]
        self.spread = data["spread"]
        self.contract_size = data["contract_size"]
        self.min_volume = data["min_volume"]
        self.max_volume = data["max_volume"]
        self.swap_long = data["swap_long"]
        self.swap_short = data["swap_short"]

    def do_something(self):
        pass


class InstrumentMT4(Instrument):
    def __init__(self,data):
        self.name = data["symbol"]
        self.points = data["points"]
        self.digits = data["digits"]
        self.spread = data["spread"] * self.points
        self.contract_size = data["contract_size"]
        self.min_volume = data["min_volume"]
        self.max_volume = data["max_volume"]
        self.swap_long = data["swap_long"]
        self.swap_short = data["swap_short"]

    def do_something(self):
        pass
