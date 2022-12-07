from Create import Create
from Process import Process
from Model import Model
from Element import Element


class SimulationBankModel():
    def __init__(self):
        c = Create(delayMean = 0.3, name = 'CREATOR', distribution = 'exp')
        p1 = Process(maxqueue = 4, delayMean = 0.3, name = 'WORKER_1', distribution = 'exp')
        p2 = Process(maxqueue = 4, delayMean = 0.3, name = 'WORKER_2', distribution = 'exp')
        
        c.nextElements = [p1, p2]
        elements = [c, p1, p2]
        model = Model(elements, displayLogs = True, loadBalancing = [p1, p2])
        model.simulation(50)

Element.id = 0
bankSimulation = SimulationBankModel()