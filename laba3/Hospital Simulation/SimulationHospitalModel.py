from Model import Model
from Create import Create
from Despose import Despose
from Process import Process
from Element import Element


class SimulationHospitalModel():
    def __init__(self):

        c = Create(delayMean = 15.0, name = 'CREATOR', distribution = 'exp')
        p1 = Process(maxqueue = 100, nChannel = 2, name = 'ПРИЙМАЛЬНЕ ВІДДІЛЕННЯ', distribution = 'exp')
        p2 = Process(maxqueue = 100, delayMean = 3.0, delayDev = 8, nChannel = 3, name = 'ШЛЯХ ДО ПАЛАТИ', distribution = 'unif')
        p3 = Process(maxqueue = 100, delayMean = 2.0, delayDev = 5, nChannel = 10, name = 'ШЛЯХ ДО ПРИЙОМУ В ЛАБОРАТОРІЮ', distribution = 'unif')
        p4 = Process(maxqueue = 100, delayMean = 4.5, delayDev = 3, nChannel = 1, name = 'ОБСЛУГОВУВАННЯ В РЕЄСТРАТУРІ ЛАБОРАТОРІЇ', distribution = 'erlanga')
        p5 = Process(maxqueue = 100, delayMean = 4.0, delayDev = 2, nChannel = 1, name = 'АНАЛІЗ', distribution = 'erlanga')
        p6 = Process(maxqueue = 100, delayMean = 2.0, delayDev = 5, nChannel = 10, name = 'ШЛЯХ ДО РЕЄСТРАТУРИ', distribution = 'unif')
        
        d1 = Despose(name = 'EXIT 1')
        d2 = Despose(name = 'EXIT 2')

        c.nextElements = [p1]
        p1.nextElements = [p2, p3]
        p2.nextElements = [d1]
        p3.nextElements = [p4]
        p4.nextElements = [p5]
        p5.nextElements = [d2, p6]
        p6.nextElements = [p1]
        
        p1.priorityTypes = [1]
        
        p1.patienPath = [[1], [2, 3]]
        p5.patienPath = [[3], [2]]
        
        elements = [c, p1, p2, p3, p4, p5, p6, d1, d2]
        
        model = Model(elements, displayLogs = True)
        model.simulation(600)

Element.id = 0
hospitalSimulation = SimulationHospitalModel()