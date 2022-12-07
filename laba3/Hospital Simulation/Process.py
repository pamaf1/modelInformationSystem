import numpy as np
from Element import Element


class Process(Element):
    def __init__(self, maxqueue = np.inf, nChannel = 1, patienPath = None, **kwargs):
        super().__init__(**kwargs)
        self.failure = 0
        self.queue = 0
        self.maxQueue = maxqueue
        self.meanQueue = self.queue
        self.nChannel = nChannel
        self.tnexts = [np.inf] * nChannel
        self.states = [0] * nChannel
        self.maxQueueLength = self.queue
        self.priorityTypes = []
        self.patienPath = patienPath
        self.queueTypes = []
        self.types = [-1] * nChannel
        self.pathToLabReceptionBefore = 0
        self.labReceptionDeltaTime = 0
        self.timeStarts = [-1] * nChannel
        self.nNewPacientType2 = 0
        self.timeStarts_queue = []
        self.finishedDeltaTime2 = 0
        
    def inAct(self, nextPatientType, startTime):
        self.nextPatientType = nextPatientType
        if self.name == 'ШЛЯХ ДО ПРИЙОМУ В ЛАБОРАТОРІЮ':
            self.labReceptionDeltaTime += self.tcurr - self.pathToLabReceptionBefore
            self.pathToLabReceptionBefore = self.tcurr
        if self.name == 'ШЛЯХ ДО РЕЄСТРАТУРИ' and nextPatientType == 2:
            self.finishedDeltaTime2 += self.tcurr - startTime
            self.nNewPacientType2 += 1

        emptyChannels = self.findEmptyChannels()
        for ind in emptyChannels:
            self.states[ind] = 1
            self.tnexts[ind] = self.tcurr + super().getDelay()
            self.types[ind] = self.nextPatientType
            self.timeStarts[ind] = startTime
            break
        else:
            if self.queue < self.maxQueue:
                self.queue += 1
                self.queueTypes.append(self.nextPatientType)
                self.timeStarts_queue.append(startTime)
                if self.queue > self.maxQueueLength:
                    self.maxQueueLength = self.queue
            else:
                self.failure += 1
            
    def outAct(self):
        super().outAct()
        currChannels = self.findCurrentChannels()
        
        for i in currChannels:
            self.tnexts[i] = np.inf
            self.states[i] = 0 

            prevNextPatientType = self.types[i]
            prevStartTime = self.timeStarts[i]
            self.types[i] = -1
            self.timeStarts[i] = -1

            if self.queue > 0:
                self.queue -= 1
                prioritetIndex = self.getIndexFromQueue()
                self.nextPatientType = self.queueTypes.pop(prioritetIndex)
                self.tnexts[i] = self.tcurr + super().getDelay()
                self.states[i] = 1
                self.types[i] = self.nextPatientType
                self.timeStarts[i] = self.timeStarts_queue.pop(prioritetIndex)

            if self.nextElements is not None:
                self.nextPatientType = 1 if self.name == 'ШЛЯХ ДО РЕЄСТРАТУРИ' else prevNextPatientType
                if self.patienPath is None:
                    nextElement = np.random.choice(self.nextElements, p = self.p)
                    nextElement.inAct(self.nextPatientType, prevStartTime)
                else:
                    for ind, path in enumerate(self.patienPath):
                        if self.nextPatientType in path:
                            nextElement = self.nextElements[ind]
                            nextElement.inAct(self.nextPatientType, prevStartTime)
                            break
                
    def getIndexFromQueue(self):
        for priorityTypesI in self.priorityTypes:
            for typeI in np.unique(self.queueTypes):
                if typeI == priorityTypesI:
                    return self.queueTypes.index(typeI)
        else:
            return 0
        
    def showInfo(self):
        super().showInfo()
        print(f'failure = {self.failure}, queue = {self.queue}, types = {self.types}')
        
    def showStatistics(self, delta):
        self.meanQueue += delta * self.queue