import numpy as np

def linear_approximation(y):
    x = np.arange(len(y))
    k, m = np.polyfit(x,y,1)
    return k, m