

class cryptoTraderAssets:
    def __init__(self, binance_interface):
        self.binance_interface = binance_interface
        self.assets = {}
        
        self._update_assets()

    def _update_assets(self):
        assets = self.binance_interface.get_client_info()

        for asset in assets["balances"]:
            symbol = asset["asset"]
            self.assets[symbol] = asset

    def get_asset(self, symbol):
        self._update_assets()
        return self.assets[symbol]

    def get_capital(self):
        self._update_assets()
        price = self.binance_interface.get()["Close"] # get closing price of crypto
        return self.assets["EUR"] + self.assets["BTC"]*price
        