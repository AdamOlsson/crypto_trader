from classes.CryptoTrader import CryptoTrader
from classes.CryptoTrader import CryptoTrader
from classes.Binance.BinanceInterface import BinanceInterface, BinanceInterfaceStub
from classes.DataSeries import DataSeries1m
from classes.Strategies.SimpleStrategies import SellWhenReturnIs10EurStrategy
from classes.Logger import Logger
from binance.spot import Spot

def getKeys():
    with open("../binance-key","r") as f:
        header = f.readline() # Don't care about header
        keys = f.readline()
        return keys.split(",")


api_key, secret_key = getKeys()
spot = Spot(key=api_key, secret=secret_key)
symbol = "ETHEUR"
asset = "ETH"

binance_interface = BinanceInterface(symbol, "1m", spot)
capital = binance_interface.get_capital(asset)

data_series = DataSeries1m()
binance_interface_stub = BinanceInterfaceStub(capital, data_series)

bi = binance_interface

logger = Logger("./logs")
strategy = SellWhenReturnIs10EurStrategy(capital, binance_interface=bi)

trader = CryptoTrader(strategy, bi, asset, logger=logger)
trader.run()