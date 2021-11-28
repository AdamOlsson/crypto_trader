from CryptoTrader import CryptoTrader
from BinanceLiveKlineData import BinanceLiveKlineData
from SimpleStrategies import SellWhenReturnIs10EurStrategy
from Logger import Logger

capital = 1700
kline_api = BinanceLiveKlineData("BTCEUR", "1m")
logger = Logger("./logs")
strategy = SellWhenReturnIs10EurStrategy(capital, logger=logger)

trader = CryptoTrader(strategy, kline_api)
trader.run()