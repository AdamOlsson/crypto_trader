import matplotlib.pyplot as plt
from datetime import datetime
from StrategyInterface import StrategyInterface

class SellWhenReturnIs10EurStrategyV2(StrategyInterface):
    # This strategy will buy crypto for the full capital and only sell
    # when the estimated gain is 10EUR. Additionally, if the value of
    # crypto is at all time high, it avoid buying until its 100EUR
    # below. V2 takes upswings into consideration.

    sell_thresh = 10
    all_time_high_threshold = 100

    def __init__(self, starting_capital):
        super().__init__(starting_capital)
        self.buy_price = None
        self.in_trade = False
        self.prev_close = 0

    def should_buy_at(self, price):
        # Only buy is price is 100EUR below all time high
        return price > self.get_all_time_high() - self.all_time_high_threshold

    def should_sell_at(self, price):
        # only sell if gain is 10EUR
        sell_value = price*self.crypto
        sell_value -= self.compute_fee(sell_value) # remove fee
        buy_value = self.buy_price*self.crypto
        
        return sell_value - buy_value > self.sell_thresh

    def step(self, datapoint):
        StrategyInterface.step(self, datapoint)
        limit_price_eur = datapoint["Close"]

        delta_close = limit_price_eur - self.prev_close 

        if not self.in_trade and self.should_buy_at(limit_price_eur):
            self.buy(limit_price_eur)
            self.buy_price = limit_price_eur
            self.in_trade = True
        elif self.in_trade and self.should_sell_at(limit_price_eur) and delta_close < -10:
            self.sell(limit_price_eur)
            self.buy_price = None
            self.in_trade = False

        self.prev_close = limit_price_eur

        return self.get_capital()


    def summary(self):
        StrategyInterface.summary(self)

class SellWhenReturnIs10EurStrategy(StrategyInterface):
    # This strategy will buy crypto for the full capital and only sell
    # when the estimated gain is 10EUR. Additionally, if the value of
    # crypto is at all time high, it avoid buying until its 100EUR
    # below.

    sell_thresh = 10
    all_time_high_threshold = 100

    def __init__(self, starting_capital):
        super().__init__(starting_capital)
        self.buy_price = None
        self.in_trade = False

    def should_buy_at(self, price):
        # Only buy is price is 100EUR below all time high
        return price > self.get_all_time_high() - self.all_time_high_threshold

    def should_sell_at(self, price):
        # only sell if gain is 10EUR
        sell_value = price*self.crypto
        sell_value -= self.compute_fee(sell_value) # remove fee
        buy_value = self.buy_price*self.crypto
        return sell_value - buy_value > self.sell_thresh

    def step(self, datapoint):
        StrategyInterface.step(self, datapoint)
        limit_price_eur = datapoint["Close"]

        if not self.in_trade and self.should_buy_at(limit_price_eur):
            self.buy(limit_price_eur)
            self.buy_price = limit_price_eur
            self.in_trade = True
        elif self.in_trade and self.should_sell_at(limit_price_eur):
            self.sell(limit_price_eur)
            self.buy_price = None
            self.in_trade = False

        return self.get_capital()


    def summary(self):
        StrategyInterface.summary(self)




class DumbStrategy(StrategyInterface):
    # This strategy will buy crypto with the full capital in one step
    # and sell all crypto the next step
    capital_history = []
    crypto_history  = []

    def __init__(self, capital):
        super().__init__(capital)
        self.in_trade = False

    def step(self, datapoint):
        limit_price_eur = datapoint["Close"]

        if not self.in_trade:
            crypto = self.buy(limit_price_eur)
            self.in_trade = True
        else:
            capital = self.sell(limit_price_eur)
            self.in_trade = False
        
        return self.get_capital()


    def summary(self):
        StrategyInterface.summary(self)
