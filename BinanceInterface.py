# Create an interface and inherit
import time
from DataSeries import DataSeries1m


class BinanceInterface():
    def __init__(self, symbol, interval, spot):
        self.symbol = symbol
        self.interval = interval
        self.spot = spot

    def get(self):
        res = self.spot.klines(self.symbol, self.interval, limit=1)[-1]
        return {"Open time":res[0],"Open":float(res[1]),"High":float(res[2]),"Low":float(res[3]),"Close":float(res[4]),"Close time":res[6]}

    def get_server_time(self):
        return self.spot.time()["serverTime"] # milliseconds

    def get_client_info(self):
        return self.spot.account()

    def buy(self):
        symbol = "BTCEUR"
        side = "BUY"
        type = "LIMIT"
        ack = self.spot.new_order_test(symbol, side, type)
        return ack

    def sell(self):
        symbol = "BTCEUR"
        side = "SELL"
        type = "LIMIT"
        ack = self.spot.new_order_test(symbol, side, type)
        return ack

    def get_capital(self):
        balances = self.spot.account()["balances"]
        assets = {}
        for asset in balances:
            symbol = asset["asset"]
            assets[symbol] = asset

        price = self.binance_interface.get()["Close"] # get closing price of crypto

        capital = self.assets["EUR"]["free"] + self.assets["BTC"]["free"]*price

        return capital


class BinanceInterfaceStub():
    maker_fee = taker_fee = 1/(100 * 10) # 0.1%
    def __init__(self, starting_capital):
        self.data_series = DataSeries1m()

        self.i = 0
        self.starting_capital = starting_capital
        self.balances = {"balances": [
            {"asset": "BTC", "free": "0.00000000",               "locked": "0.00000000"},
            {"asset": "EUR", "free": str(self.starting_capital), "locked": "0.00000000"}
        ]}

    def get(self):
        ret = self.data_series[self.i]
        self.i +=1
        return ret

    def get_server_time(self):
        return self._get_current()["Open time"]

    def get_client_info(self):
        return self.balances

    def _get_current(self):
        return self.data_series[self.i]

    def compute_fee(self, amount):
        return amount*self.maker_fee

    def set_asset_balance(self, symbol, value):
        balances = self.balances["balances"]
        for asset in balances:
            if symbol == asset["asset"]:
                asset["free"] = str(value)
                break

    def get_asset_balance(self, symbol):
        balances = self.balances["balances"]
        for asset in balances:
            if symbol == asset["asset"]:
                return float(asset["free"])

    def get_capital(self):
        balances = self.balances["balances"]
        assets = {}
        for asset in balances:
            symbol = asset["asset"]
            assets[symbol] = asset

        price = self._get_current()["Close"] # get closing price of crypto
        capital = float(assets["EUR"]["free"]) + float(assets["BTC"]["free"])*price

        return capital

    def buy(self):

        balances = self.balances["balances"]
        assets = {}
        for asset in balances:
            symbol = asset["asset"]
            assets[symbol] = asset

        eur = float(assets["EUR"]["free"])
        
        price = self._get_current()["Open"]
        fee_eur = self.compute_fee(eur)
        crypto = (eur - fee_eur)/price

        self.set_asset_balance("BTC", crypto)
        self.set_asset_balance("EUR", 0)

        return {}

    def sell(self):

        balances = self.balances["balances"]
        assets = {}
        for asset in balances:
            symbol = asset["asset"]
            assets[symbol] = asset

        btc = float(assets["BTC"]["free"])

        price = self._get_current()["Open"]
        eur = price*btc
        eur -= self.compute_fee(eur)

        self.set_asset_balance("BTC", 0)
        self.set_asset_balance("EUR", eur)

        return {}