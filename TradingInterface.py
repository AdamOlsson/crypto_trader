
class TradingInterface:
    def __init__(self, binance_interface):
        self.binance_interface = binance_interface

    def buy(self):
        self.binance_interface.buy()

    def sell(self):
        self.binance_interface.sell()