from datetime import datetime
from Strategies import Strategies
import numpy as np

class Simulation:
    def __init__(self, strategies: Strategies):
        self.strategies = strategies
        self.top_n_to_display = min(3, len(self.strategies))

        self.capital_format = "{:>20} EUR, " * self.top_n_to_display
        self.step_print_format = "[{:>5}/{:>5}] {} Top {} capital: " + self.capital_format

    def run(self, data_series):
        length = len(data_series) -1
        print("\n")
        for i, datapoint in enumerate(data_series):
            capital = self.strategies.step(datapoint)

            is_bankrup = max(capital) < 10.0

            capital = np.array(capital)
            best_indices = (-capital).argsort()[:self.top_n_to_display]

            timestamp_ms = datapoint["Close time"]
            timestamp = datetime.utcfromtimestamp(timestamp_ms/1000).strftime('%Y-%m-%d %H:%M')

            if is_bankrup:
                print(self.step_print_format.format(i, length, timestamp, self.top_n_to_display, *capital[best_indices]))
                print("\n")
                print("Early stop. Bankrupt!")
                break
            else:
                print(self.step_print_format.format(i, length, timestamp, self.top_n_to_display, *capital), end="\r")

        print("\nSummary:")
        self.strategies.summary()

        return self.strategies.get_capital()