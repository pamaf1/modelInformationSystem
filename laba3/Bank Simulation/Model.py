import numpy as np
from Despose import Despose
from Process import Process

class Model():
    def __init__(self, elements = [], displayLogs = False, loadBalancing = None):
        self.elements = elements
        self.tnext = 0
        self.event = elements[0]
        self.tcurr = self.tnext
        self.displayLogs = displayLogs
        self.meanBanClients = 0
        self.linesChange = 0
        self.loadBalancing = loadBalancing
        
    def simulation(self, time):
        self.timeModeling = time
        while self.tcurr < self.timeModeling:
            self.tnext = np.inf

            for element in self.elements:
                tnextMin = np.min(element.tnexts)
                if tnextMin < self.tnext and not isinstance(element, Despose):
                    self.event = element
                    self.tnext = tnextMin

            self.determineMeanBankClients(self.tnext - self.tcurr)

            if self.displayLogs:
                print(f'\nIt is time for event in {self.event.name}, time = {np.round(self.tnext, 9)}')
            
            for element in self.elements:
                element.showStatistics(self.tnext - self.tcurr)
            
            self.tcurr = self.tnext
            for element in self.elements:
                element.tcurr = self.tcurr
            
            self.event.outAct()
            
            for element in self.elements:
                if self.tcurr in element.tnexts:
                    element.outAct()

            self.displayInfo()

        return self.displayStatistic()
        
    def displayInfo(self):
        for element in self.elements:
            element.displayInfo()
                    
    def determineMeanBankClients(self, delta):
        temp = self.loadBalancing[0].queue + self.loadBalancing[1].queue + self.loadBalancing[0].states[0] + self.loadBalancing[1].states[0]
        self.meanBanClients += temp * delta

    def displayStatistic(self):
        nProcessors = 0
        failsAccumulator = 0
        meanLoadAccumulator = 0
        meanOutGoingAccumulator = 0
        meanBankTimeAccumulator = 0
        meanQueueLengthAccumulator = 0

        print('-----RESULT-----')
        
        for elem in self.elements:
            elem.displayStatistic()
            if isinstance(elem, Process):
                nProcessors += 1
                meanLoad = elem.quantity / self.timeModeling
                meanLoadAccumulator += meanLoad
                meanOutGoingAccumulator += elem.outGoingDelta / elem.quantity
                meanBankTimeAccumulator += elem.bankTimeDelta / elem.quantity
                meanQueue = elem.meanQueue / self.tcurr
                meanQueueLengthAccumulator += meanQueue
                fails = elem.failure / (elem.quantity + elem.failure) if (elem.quantity + elem.failure) != 0 else 0
                failsAccumulator += fails
                print(f"Середнє завантаження касира: {meanLoad}")
                print(f"Середня довжина черги: {meanQueue}")
                print(f"Середній час відправлення = {elem.outGoingDelta / elem.quantity}")
                print(f"Імовірність відмови: {fails}\n")
                    
        generalMeanLoad = meanLoadAccumulator / nProcessors
        meanBanClients = self.meanBanClients / self.tcurr
        generalMeanTimeOfDeparture = meanOutGoingAccumulator / nProcessors
        generalMeanBankTime = meanBankTimeAccumulator / nProcessors
        generalMeanQueue = meanQueueLengthAccumulator / nProcessors
        generalFails = failsAccumulator / nProcessors
        
        if self.displayLogs:
            print(f"1) Середнє завантаження кожного касира: {generalMeanLoad}")
            print(f"2) Cереднє число клієнтів у банку: {meanBanClients}")
            print(f"3) Cередній інтервал часу між від'їздами клієнтів від вікон: {generalMeanTimeOfDeparture}")
            print(f"4) Cередній час перебування клієнта в банку: {generalMeanBankTime}")
            print(f"5) Cереднє число клієнтів у кожній черзі: {generalMeanQueue}")
            print(f"6) Відсоток клієнтів, яким відмовлено в обслуговуванні: {generalFails}")
            print(f"7) Число змін під'їзних смуг: {self.linesChange}")