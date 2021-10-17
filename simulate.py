from DataSeries import DataSeries15m, DataSeries1m
from SimpleStrategies import DumbStrategy, SellWhenReturnIs10EurStrategy, SellWhenReturnIs10EurStrategyV2
from ApproximationStrategies import LinearApproximationStrategy
from Simulation import Simulation
from Strategies import Strategies

ds = DataSeries1m()

capital = 1000 # EUR
linearApproximationStrategy = LinearApproximationStrategy(capital)
sellWhenReturnIs10EurStrategy = SellWhenReturnIs10EurStrategy(capital)

strategies = Strategies([linearApproximationStrategy, sellWhenReturnIs10EurStrategy])
simulation = Simulation(strategies)

simulation.run(ds)