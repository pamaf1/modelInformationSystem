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
        globalMeanQueueAccumulator = 0
        globalMeanFailureAccumulator = 0
        globalMeanLoadAccumulator = 0
        print('\n----------RESULTS----------')
        
        for e in self.elements:
            e.showStatistic()
            if isinstance(e, Process):
                nProcessors += 1
                meanQueue = e.meanQueue / self.tcurr
                failureProbability = e.failure / (e.failure + e.quantity) if (e.failure + e.quantity) != 0 else 0
                meanLoad = e.processTimeDelta / self.tcurr
                globalMeanQueueAccumulator += meanQueue
                globalMeanFailureAccumulator += failureProbability
                globalMeanLoadAccumulator += meanLoad
                
                if self.displayLogs:
                    print(f"Mean length of queue = {meanQueue}")
                    print(f"Failure Probability = {failureProbability}")
                    print(f"Average Loading: {np.round(meanLoad, 5)}\n")
                
        globalMeanQueue = globalMeanQueueAccumulator / nProcessors
        globalMeanFailure = globalMeanFailureAccumulator / nProcessors
        globalMeanLoad = globalMeanLoadAccumulator / nProcessors
        
        if self.displayLogs:
            print(f"Average Global Queue: {globalMeanQueue}")
            print(f"Average Global Failure: {globalMeanFailure}")
            print(f"Average Global Loading: {np.round(globalMeanLoad, 5)}\n")
        
        return { "global mean load": np.round(globalMeanLoad, 5), "global mean queue": globalMeanQueue, "global mean failure": globalMeanFailure }

    def simulation(self, time1):
        self.timeModeling = time1
        
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