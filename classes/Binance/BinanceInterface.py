
import math


class BinanceInterface():
    def __init__(self, symbol, interval, spot):
        self.symbol = symbol
        self.interval = interval
        self.spot = spot

    def get(self):
        try:
            res = self.spot.klines(self.symbol, self.interval, limit=1)[-1]
            return {"Open time":res[0],"Open":float(res[1]),"High":float(res[2]),"Low":float(res[3]),"Close":float(res[4]),"Close time":res[6]}
        except:
            return {}

    def get_server_time(self):
        return self.spot.time()["serverTime"] # milliseconds

    def get_client_info(self):
        return self.spot.account()

    def get_asset_balance(self, symbol):
        balances = self.spot.account()["balances"]
        for asset in balances:
            if symbol == asset["asset"]:
                return float(asset["free"])

    def buy(self):

        kline_data = self.get()
        
        if not bool(kline_data):
            pass #error handling

        closing_price = kline_data["Close"]
        eur_balance = self.get_asset_balance("EUR")
        quantity = eur_balance/closing_price - 0.0002 # margin for price variations

        params = {
            'symbol': self.symbol,
            'side': 'BUY',
            'type': 'LIMIT',
            'timeInForce': 'GTC',
            'quantity': '%.4f' % quantity,
            'price': closing_price
        }
        try:
            ack = self.spot.new_order(**params)
        except:
            self.spot.cancel_open_orders(self.symbol)

        return ack

    def truncate(self, f, n):
        return math.floor(f * 10 ** n) / 10 ** n

    def sell(self, asset):
        
        price = self.get()["Close"]
        asset_balance = self.get_asset_balance(asset)

        params = {
            'symbol': self.symbol,
            'side': 'SELL',
            'type': 'LIMIT',
            'timeInForce': 'GTC',
            'quantity': self.truncate(asset_balance, 4),
            'price': price
        }

        try:
            ack = self.spot.new_order(**params)
        except:
            self.spot.cancel_open_orders(self.symbol)

        return ack

    def get_capital(self, target_asset):
        balances = self.spot.account()["balances"]
        assets = {}
        for asset in balances:
            symbol = asset["asset"]
            assets[symbol] = asset

        price = self.get()["Close"] # get closing price of crypto

        capital = float(assets["EUR"]["free"]) + float(assets[target_asset]["free"])*price

        return capital

    def getOrder(self, orderId):
        params = {
            'symbol': self.symbol,
            'orderId': orderId
            # 'timestamp': transactTime
        }
        order = self.spot.get_order(**params)
        return order


class BinanceInterfaceStub():
    maker_fee = taker_fee = 1/(100 * 10) # 0.1%
    def __init__(self, starting_capital, data_series):
        self.data_series = data_series

        self.i = 0
        self.starting_capital = starting_capital
        self.balances = {"balances": [
            {"asset": "BTC", "free": "0.00000000",               "locked": "0.00000000"},
            {"asset": "ETH", "free": "0.00000000",               "locked": "0.00000000"},
            {"asset": "EUR", "free": str(self.starting_capital), "locked": "0.00000000"}
        ]}

    def get(self):
        self.i +=1
        ret = self.data_series[self.i]
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

    def get_capital(self, target_asset):
        balances = self.balances["balances"]
        assets = {}
        for asset in balances:
            symbol = asset["asset"]
            assets[symbol] = asset

        price = self._get_current()["Close"] # get closing price of crypto
        capital = float(assets["EUR"]["free"]) + float(assets[target_asset]["free"])*price

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

        self.set_asset_balance("BTC", crypto) # TODO Will not work
        self.set_asset_balance("EUR", 0)      # TODO Will not work

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