import random
import numpy as np

def exp(timeMean):
    a = 0.0
    while a == 0:
        a = random.random()
    a = -timeMean * np.log(a)
    return a

def uniform(timeMin, timeMax):
    a = 0.0
    while a == 0:
        a = random.random()
    a = timeMin + a * (timeMax - timeMin)
    return a

def norm(timeMean, timeDeviation):
    return timeMean + timeDeviation * random.gauss(0.0, 1.0)
