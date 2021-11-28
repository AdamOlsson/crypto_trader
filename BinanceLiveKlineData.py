from binance.spot import Spot

# Create an interface and inherit
class BinanceLiveKlineData():
    def __init__(self, symbol, interval):
        self.symbol = symbol
        self.interval = interval
        self.client = Spot()

    def get(self):
        res = self.client.klines(self.symbol, self.interval, limit=1)[-1]
        return {"Open time":res[0],"Open":float(res[1]),"High":float(res[2]),"Low":float(res[3]),"Close":float(res[4]),"Close time":res[6]}

    def get_server_time(self):
        return self.client.time()["serverTime"] # milliseconds




