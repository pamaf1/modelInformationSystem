from Model import Model
from Create import Create
from Process import Process


class SimModel1():
    def __init__(self):
        c = Create(delayMean = 1.0, name = 'CREATOR', distribution = 'exp')
        p = Process(maxqueue = 2, delayMean = 10.0, name = 'PROCESS_1', distribution = 'exp')

        c.nextElements = [p]
        elements = [c, p]
        model = Model(elements, displayLogs = True)
        model.simulation(100)