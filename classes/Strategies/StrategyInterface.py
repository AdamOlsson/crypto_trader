import matplotlib.pyplot as plt
from datetime import datetime

class StrategyInterface:
    maker_fee = taker_fee = 1/(100 * 10) # 0.1%

    def __init__(self, starting_capital, logger=None, system_is_live=True):
        self.price_history = []
        self.number_of_trades = 0
        self.capital_before_buy = 0
        self.capital = float(starting_capital)
        self.crypto = float(0)
        self.capital_history = []
        self.return_from_sell = 0
        self.monthly_earning_dict = {}
        self.all_time_high = 0
        self.all_time_high_history = []
        self.starting_capital = starting_capital
        self.in_trade = False
        self.logger = logger
        self.system_is_live = system_is_live
        self.history_buy = []
        self.history_sell = []
        self.step_count = 0


    def step(self, datapoint) -> float:
        limit_price_eur = datapoint["Close"]
        timestamp_ms = datapoint["Close time"]

        monthly_earning_bucket = datetime.utcfromtimestamp(timestamp_ms/1000).strftime('%Y-%m')

        if not monthly_earning_bucket in self.monthly_earning_dict:
            self.monthly_earning_dict[monthly_earning_bucket] = 0
            self.current_bucket = monthly_earning_bucket


        self.all_time_high = max(self.all_time_high, limit_price_eur)

        if not self.system_is_live:
            self.step_count += 1
            self.price_history.append(limit_price_eur)
            self.all_time_high_history.append(self.all_time_high)


    def get_all_time_high(self):
        return self.all_time_high

    def compute_fee(self, amount):
        return amount*self.maker_fee

    def buy(self, datapoint):
        price = datapoint["Open"]
        fee_eur = self.compute_fee(self.capital)
        self.crypto = (self.capital - fee_eur)/price

        self.capital_before_buy = self.capital
        self.capital = 0
        self.in_trade = True

        if self.logger != None:
            self.logger.log_buy(datapoint, self.crypto)
        
        if not self.system_is_live:
            self.history_buy.append((self.step_count, price))

        return self.crypto

    def sell(self, datapoint):
        def compute_earning_from_prev_sell():
            return self.return_from_sell - self.capital_before_buy

        price = datapoint["Open"]

        value_eur = price*self.crypto
        self.capital = value_eur - self.compute_fee(value_eur)

        self.crypto = 0

        self.number_of_trades += 1
        self.return_from_sell = self.capital

        earning = compute_earning_from_prev_sell()
        self.monthly_earning_dict[self.current_bucket] += earning

        self.in_trade = False

        if not self.system_is_live:
            self.capital_history.append(self.capital)
            self.history_sell.append((self.step_count, price))

        if self.logger != None:
            self.logger.log_sell(datapoint, self.capital)

        return self.capital

    def get_capital(self):
        return self.capital if self.capital != 0 else self.capital_before_buy
    
    def get_in_trade(self):
        return self.in_trade

    def summary(self):
        cap = self.capital if self.capital != 0 else self.capital_before_buy
        print("Capital: {} EUR".format(cap))
        print("Number of trades {}".format(self.number_of_trades))

        print("Monthly earnings")
        last_month_earning = self.starting_capital
        for k, v in self.monthly_earning_dict.items():
            print("{:>5}: {:>16} EUR ({}%)".format(k, v, v/last_month_earning))
            last_month_earning = v+self.starting_capital

        plt.plot(self.capital_history)
        plt.title("Capital History")
        plt.ylabel("Capital (EUR)")
        plt.xlabel("Number of Trades")
        plt.savefig("./summary.png")
        plt.cla() # clear plots

        plt.plot(self.all_time_high_history, label="All time high")
        plt.plot(self.price_history, label="Close")

        steps, buy_price = list(zip(*self.history_buy))
        plt.scatter(steps, buy_price, c="green")

        steps, sell_price = list(zip(*self.history_sell))
        plt.scatter(steps, sell_price, c="red")

        plt.legend()
        plt.ylabel("Capital (EUR)")
        plt.xlabel("Steps")
        plt.savefig("./all_time_high.png")
        plt.cla() # clear plots