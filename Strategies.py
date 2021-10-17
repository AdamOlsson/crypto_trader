from StrategyInterface import StrategyInterface

class Strategies(StrategyInterface):
    def __init__(self, strategies):
        self.strategies = strategies
        self.capital = [0] * len(self.strategies)

    def step(self, datapoint):
        for i, strat in enumerate(self.strategies):
            self.capital[i] = strat.step(datapoint)

        return self.capital
    
    def __getitem__(self, i):
        return self.strategies[i]

    def __len__(self):
        return len(self.capital)

    def summary(self, i=-1):
        if i == -1:
            for i, strat in enumerate(self.strategies):
                print("Strategy {}".format(type(strat).__name__))
                strat.summary()
                print("\n")
        else:
            strat = self.strategies[i]
            print("Strategy {}".format(type(strat).__name__))
            strat.summary()
            print("\n")
    
    def get_capital(self):
        return [strat.get_capital() for strat in self.strategies]