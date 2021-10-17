from StrategyInterface import StrategyInterface
from Window import Window
from util import linear_approximation

class LinearApproximationStrategy(StrategyInterface):
    # Strategy makes a linear apporximation based on the previous
    # *window_size* points. Depending on the slope, a decision is 
    # to either sell or buy is made

    def __init__(self, starting_capital, window_size=15, k_thresh_buy=1, k_thresh_sell=0):
        super().__init__(starting_capital)
        self.k_thresh_buy = k_thresh_buy
        self.k_thresh_sell = k_thresh_sell
        self.window_size = window_size
        self.window = Window(self.window_size)
        self.in_trade = False

    def should_buy(self, k):
        return k > self.k_thresh_buy

    def should_sell(self, k):
        return k < self.k_thresh_sell

    def step(self, datapoint):
        StrategyInterface.step(self, datapoint)

        window = self.window
        in_trade = self.in_trade

        window.add(datapoint["Open"])
        limit_price_eur = datapoint["Open"]

        if window.is_full():
            k, m = linear_approximation(window)

            if not in_trade and self.should_buy(k):
                self.buy(limit_price_eur)
                self.in_trade = True
            elif in_trade and self.should_sell(k):
                self.sell(limit_price_eur)
                self.in_trade = False

        return self.get_capital()
    
    def summary(self):
        StrategyInterface.summary(self)
        print("Parameters: window_size={}, k_thresh_buy={}, k_thresh_sell={}".format(
            self.window_size,
            self.k_thresh_buy,
            self.k_thresh_sell
        ))



