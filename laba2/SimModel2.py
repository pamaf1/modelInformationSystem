from Model import Model
from Process import Process
from Create import Create
from Despose import Despose


class SimModel2():
    def __init__(self):
        c = Create(delayMean = 1, name = 'CREATOR', distribution = 'exp')
        p1 = Process(maxqueue = 2, delayMean = 1.0, name = 'PROCESS_1', distribution = 'exp')
        p2 = Process(maxqueue = 2, delayMean = 1.0, name = 'PROCESS_2', distribution = 'exp')
        p3 = Process(maxqueue = 2, delayMean = 1.0, name = 'PROCESS_3', distribution = 'exp')
        d = Despose(delayMean = 0, name = 'DESPOSER')
        
        c.nextElements = [p1]
        p1.nextElements = [p2]
        p2.nextElements = [p3]
        p3.nextElements = [d]
        
        c.p = [1]
        p1.p = [1]
        p2.p = [1]
        p3.p = [1]
        
        elements = [c, p1, p2, p3, d]

        model = Model(elements, displayLogs = True)
        model.simulation(50)