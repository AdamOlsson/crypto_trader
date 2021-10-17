import matplotlib.pyplot as plt
from datetime import datetime

class StrategyInterface:
    maker_fee = taker_fee = 1/(100 * 10) # 0.1%

    def __init__(self, starting_capital):
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


    def step(self, datapoint) -> float:
        limit_price_eur = datapoint["Close"]
        timestamp_ms = datapoint["Close time"]

        monthly_earning_bucket = datetime.utcfromtimestamp(timestamp_ms/1000).strftime('%Y-%m')

        if not monthly_earning_bucket in self.monthly_earning_dict:
            self.monthly_earning_dict[monthly_earning_bucket] = 0
            self.current_bucket = monthly_earning_bucket

        self.price_history.append(limit_price_eur)

        self.all_time_high = max(self.all_time_high, limit_price_eur)
        self.all_time_high_history.append(self.all_time_high)


    def get_all_time_high(self):
        return self.all_time_high

    def compute_fee(self, amount):
        return amount*self.maker_fee

    def buy(self, price:float):
        fee_eur = self.compute_fee(self.capital)
        self.crypto = (self.capital - fee_eur)/price

        self.capital_before_buy = self.capital
        self.capital = 0
        return self.crypto

    def sell(self, price:float):
        def compute_earning_from_prev_sell():
            return self.return_from_sell - self.capital_before_buy

        value_eur = price*self.crypto
        self.capital = value_eur - self.compute_fee(value_eur)

        self.crypto = 0
        self.capital_history.append(self.capital)
        self.number_of_trades += 1
        self.return_from_sell = self.capital

        earning = compute_earning_from_prev_sell()
        self.monthly_earning_dict[self.current_bucket] += earning

        return self.capital

    def get_capital(self):
        return self.capital if self.capital != 0 else self.capital_before_buy

    def summary(self):
        cap = self.capital if self.capital != 0 else self.capital_before_buy
        print("Capital: {} EUR".format(cap))
        print("Number of trades {}".format(self.number_of_trades))

        print("Monthly earnings")
        for k, v in self.monthly_earning_dict.items():
            print("{:>5}: {:>16} EUR".format(k, v))

        plt.plot(self.capital_history)
        plt.title("Capital History")
        plt.ylabel("Capital (EUR)")
        plt.xlabel("Number of Trades")
        plt.savefig("./summary.png")
        plt.cla() # clear plots

        plt.plot(self.all_time_high_history, label="All time high")
        plt.plot(self.price_history, label="Close")
        plt.legend()
        plt.ylabel("Capital (EUR)")
        plt.xlabel("Steps")
        plt.savefig("./all_time_high.png")
        plt.cla() # clear plots