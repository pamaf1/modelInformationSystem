import numpy as np
from Element import Element


class Process(Element):
    def __init__(self, maxqueue = np.inf, **kwargs):
        super().__init__(**kwargs)
        self.outGoingDelta = 0
        self.outGoingTimeBefore = 0
        self.bankTimeDelta = 0
        self.bankTime = 0
        self.maxQueue = maxqueue
        self.failure = 0
        self.queue = 0
        self.meanQueue = self.queue
        self.tnexts = [np.inf]
        self.states = [0]

        
    def inAct(self):
        emptyChannels = self.EmptyChannels()
        for ind in emptyChannels:
            self.bankTime = self.tcurr
            self.states[ind] = 1
            self.tnexts[ind] = self.tcurr + super().getDelay()
            break
        else:
            if self.queue < self.maxQueue:
                self.queue += 1
            else:
                self.failure += 1
            
    def outAct(self):
        super().outAct()
        currentChannels = self.CurrentChannels()

        for i in currentChannels:
            self.tnexts[i] = np.inf
            self.states[i] = 0 
            
            self.outGoingDelta += self.tcurr - self.outGoingTimeBefore
            self.outGoingTimeBefore = self.tcurr

            self.bankTimeDelta += self.tcurr - self.bankTime

            if self.queue > 0:
                self.queue -= 1
                self.states[i] = 1
                self.tnexts[i] = self.tcurr + super().getDelay()
            elif self.nextElements is not None:
                nextElement = np.random.choice(self.nextElements, p = self.p)
                nextElement.inAct()
        
    def displayInfo(self):
        super().displayInfo()
        print(f'failure = {self.failure}, queue = {self.queue}')
        
    def showStatistics(self, delta):
        self.meanQueue += delta * self.queue