from CryptoTrader import CryptoTrader
from BinanceInterface import BinanceInterface, BinanceInterfaceStub
from Strategies.SimpleStrategies import SellWhenReturnIs10EurStrategy
from Logger import Logger
from binance.spot import Spot

def getKeys():
    with open("../binance-key","r") as f:
        header = f.readline() # Don't care about header
        keys = f.readline()
        return keys.split(",")


api_key, secret_key = getKeys()
spot = Spot(key=api_key, secret=secret_key)

binance_interface = BinanceInterface("BTCEUR", "1m", spot)
capital = binance_interface.get_capital()
binance_interface_stub = BinanceInterfaceStub(capital)

bi = binance_interface_stub

logger = Logger("./logs")
strategy = SellWhenReturnIs10EurStrategy(capital, logger=logger, binance_interface=bi)

trader = CryptoTrader(strategy, bi)
trader.run()