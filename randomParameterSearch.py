from DataSeries import DataSeries1m
from ApproximationStrategies import LinearApproximationStrategy
from Simulation import Simulation
from Strategies import Strategies
from random import randint
import numpy as np

ds = DataSeries1m()

capital = 1000 # EUR
strats = []
for i in range(70):
    window_size   = randint(1,60)
    k_thresh_buy  = randint(-10, 10)
    k_thresh_sell = randint(-10,10)
    strats.append(LinearApproximationStrategy(
        capital,
        window_size=window_size,
        k_thresh_buy=k_thresh_buy,
        k_thresh_sell=k_thresh_sell))

strategies = Strategies(strats)
simulation = Simulation(strategies)

capital = simulation.run(ds)

capital = np.array(capital)

n = 2

indices = (-capital).argsort()[:n]

print("### Random Search {} Best Results ###".format(n))
for i in indices:
    strategies.summary(i)

