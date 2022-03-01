from class.Window import Window
from class.DataSeries import DataSeries1m

import matplotlib.pyplot as plt
import numpy as np

step_print_format = "[{:>5}/{:>5}]"

def linear_approximation(y):
    x = np.arange(len(y))
    k, m = np.polyfit(x,y,1)
    return k, m


window_size = 15
window = Window(window_size)
data_series = DataSeries1m()

data_series_len = len(data_series)

high = []
opn = []
low  = []

ks = []

for i, datapoint in enumerate(data_series):
    print(step_print_format.format(i, data_series_len), end="\r")

    window.add(datapoint["Open"])
    high.append(datapoint["High"])
    opn.append(datapoint["Open"])
    low.append(datapoint["Low"])

    if window.is_full():
        k, m = linear_approximation(window)
        ks.append(k)
        #lin_approx = np.arange(len(window))*k + m
        #x = np.arange(i-(window_size), i)
        #plt.plot(x, lin_approx)

high = np.array(high)
opn = np.array(opn)
low = np.array(low)

#plt.plot(high, label="High")
#plt.plot(opn, label="Open")
#plt.plot(low, label="Low")
plt.plot(ks)

plt.legend()
plt.show()