import numpy as np
from Process import Process
from Despose import Despose


class Model():
    def __init__(self, elements = [], displayLogs = False):
        self.tnext = 0
        self.tcurr = self.tnext
        self.event = elements[0]
        self.elements = elements
        self.displayLogs = displayLogs
        
    def simulation(self, time):
        self.timeModeling = time
        while self.tcurr < self.timeModeling:
            self.tnext = np.inf
            for element in self.elements:
                tnextMin = np.min(element.tnexts) 
                if tnextMin < self.tnext and not isinstance(element, Despose):
                    self.event = element
                    self.tnext = tnextMin

            if self.displayLogs:
                print(f'\nIt is time for event in {self.event.name}, time = {np.round(self.tnext, 9)}')

            for element in self.elements:
                element.showStatistics(self.tnext - self.tcurr)
                

            self.tcurr = self.tnext
            for element in self.elements:
                element.tcurr = self.tcurr
            
            self.event.outAct() 
            
            for e in self.elements:
                if self.tcurr in e.tnexts:
                    e.outAct()

            self.showInfo()

        return self.dispalyStatistic()
        
    def showInfo(self):
        for element in self.elements:
            element.showInfo()
            
    def dispalyStatistic(self):
        nProcessors = 0
        nFinished = 0
        meanFinishingTimeAccumulator = 0
        meanComingToLab = 0
        failsAccumulator = 0
        print('-----RESULT-----')
        
        for elem in self.elements:
            elem.dispalyStatistic()
            if isinstance(elem, Process):
                nProcessors += 1
                meanQueue = elem.meanQueue / self.tcurr
                mean_load = elem.quantity / self.timeModeling
                fails = elem.failure / (elem.quantity + elem.failure) if (elem.quantity + elem.failure) != 0 else 0
                failsAccumulator += fails
                    
                if elem.name == 'ШЛЯХ ДО ПРИЙОМУ В ЛАБОРАТОРІЮ':
                    meanComingToLab = elem.labReceptionDeltaTime / elem.quantity
                if elem.name == 'ШЛЯХ ДО РЕЄСТРАТУРИ':
                    print(f'Середній час перебування для пацієнтів типу 2: {elem.finishedDeltaTime2 / elem.nNewPacientType2 if elem.nNewPacientType2 != 0 else np.inf}')

                print(f"Середнє завантаження: {mean_load}")
                print(f"Середня довжина черги: {meanQueue}")
                print(f"Імовірність відмови: {fails}\n")

            elif isinstance(elem, Despose):
                nFinished += elem.quantity
                sumFinishedDeltaTime = elem.finishTime1Delta + elem.finishTime2Delta + elem.finishTime3Delta
                meanFinishingTimeAccumulator += sumFinishedDeltaTime
                print(f'Середній час перебування для пацієнтів типу 1: {elem.finishTime1Delta / elem.nType1 if elem.nType1 != 0 else np.inf}')
                print(f'Середній час перебування для пацієнтів типу 3: {elem.finishTime3Delta / elem.nType3 if elem.nType3 != 0 else np.inf}\n')
        
        if self.displayLogs:
            print(f'Cередній час завершення: {meanFinishingTimeAccumulator / nFinished}')
            print(f'Cередній інтервал часу між прибуттям хворих до лабораторії: {meanComingToLab}')
            print(f"Відсоток пацієнтів, яким відмовлено в обслуговуванні: {failsAccumulator / nProcessors}")