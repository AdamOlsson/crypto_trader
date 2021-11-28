from DataSeries import DataSeries1m
from ApproximationStrategies import LinearApproximationStrategy
from SimpleStrategies import SellWhenReturnIs10EurStrategy
from Simulation import Simulation
from Strategies import Strategies
from random import randint
import numpy as np

ds = DataSeries1m()

capital = 1000 # EUR
strats = []
window_sizes = [15, 60, 60*2, 60*24, 60*24*2, 60*24,60*24*7] # minutes
denoms = [i for i in range(1,10)]
for w in window_sizes:
    for d in denoms:
        strats.append(SellWhenReturnIs10EurStrategy(
            capital,
            window_size=w,
            denominator=d
            ))

strategies = Strategies(strats)
simulation = Simulation(strategies)

capital = simulation.run(ds)

capital = np.array(capital)

n = 3

indices = (-capital).argsort()[:n]

print("### Random Search {} Best Results ###".format(n))
for i in indices:
    strategies.summary(i)

