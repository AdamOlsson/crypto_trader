from DataSeries import DataSeries15m, DataSeries1m, DataSeries1mETHEUR
from Strategies.SimpleStrategies import DumbStrategy, SellWhenReturnIs10EurStrategy, SellWhenReturnIs10EurStrategyV2
from Strategies.ApproximationStrategies import LinearApproximationStrategy
from Simulation import Simulation
from Strategies import Strategies

ds = DataSeries1m()
#ds = DataSeries1mETHEUR()

capital = 1000 # EUR
linearApproximationStrategy = LinearApproximationStrategy(capital)
sellWhenReturnIs10EurStrategy = SellWhenReturnIs10EurStrategy(capital, system_is_live=False)

strategies = Strategies([sellWhenReturnIs10EurStrategy])
simulation = Simulation(strategies)

simulation.run(ds)