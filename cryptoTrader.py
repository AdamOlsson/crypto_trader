from CryptoTrader import CryptoTrader
from BinanceInterface import BinanceInterface, BinanceInterfaceStub
from SimpleStrategies import SellWhenReturnIs10EurStrategy
from Logger import Logger
from binance.spot import Spot

def getKeys():
    with open("../binance-key","r") as f:
        header = f.readline() # Don't care about header
        keys = f.readline()
        return keys.split(",")


api_key, secret_key = getKeys()
spot = Spot(key=api_key, secret=secret_key)

capital = 1700
binance_interface = BinanceInterface("BTCEUR", "1m", spot)
binance_interface_stub = BinanceInterfaceStub(capital)

logger = Logger("./logs")
strategy = SellWhenReturnIs10EurStrategy(capital, logger=logger, binance_interface=binance_interface_stub)

trader = CryptoTrader(strategy, binance_interface_stub)
trader.run()