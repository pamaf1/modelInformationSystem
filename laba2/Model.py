import numpy as np
from Despose import Despose
from Process import Process


class Model():
    def __init__(self, elements=[], displayLogs=False):
        self.elements = elements
        self.tnext = 0
        self.event = elements[0]
        self.tcurr = self.tnext
        self.displayLogs = displayLogs
        
    def displayInfo(self):
        for element in self.elements:
            element.displayInfo()
            
    def showStatistic(self):
        nProcessors = 0
        globalMeanLoadAccumulator = 0
        print('\n----------RESULTS----------')
        
        for e in self.elements:
            e.showStatistic()
            if isinstance(e, Process):
                nProcessors += 1
                meanQueue = e.meanQueue / self.tcurr
                failureProbability = e.failure / (e.failure + e.quantity) if (e.failure + e.quantity) != 0 else 0
                meanLoad = e.quantity / self.timeModeling
                globalMeanLoadAccumulator += meanLoad
                
                if self.displayLogs:
                    print(f"Mean length of queue = {meanQueue}")
                    print(f"Failure Probability = {failureProbability}")
                    print(f"Average Loading: {meanLoad}\n")
                
        globalMeanLoad = globalMeanLoadAccumulator / nProcessors
        
        if self.displayLogs:
            print(f"Average Global Loading: {globalMeanLoad}\n")
        
        return { "global mean load": globalMeanLoad }

    def simulation(self, time):
        self.timeModeling = time
        while self.tcurr < self.timeModeling:
            self.tnext = np.inf

            for element in self.elements:
                tnextMin = np.min(element.tnexts)
                if tnextMin < self.tnext and not isinstance(element, Despose):
                    self.tnext = tnextMin
                    self.event = element

            if self.displayLogs:
                print(f'\nIt is time for event in {self.event.name}, time = {np.round(self.tnext, 9)}')
            
            for element in self.elements:
                element.doStatistics(self.tnext - self.tcurr)
                
            self.tcurr = self.tnext
            for element in self.elements:
                element.tcurr = self.tcurr
            
            self.event.outAct()

            for element in self.elements:
                if self.tcurr in element.tnexts:
                    element.outAct()

            self.displayInfo()

        return self.showStatistic()