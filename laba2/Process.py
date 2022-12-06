import numpy as np
from Element import Element


class Process(Element):
    def __init__(self, maxqueue = np.inf, n_channel = 1, **kwargs):
        super().__init__(**kwargs)
        self.failure = 0
        self.queue = 0
        self.max_queue = maxqueue
        self.meanQueue = self.queue
        self.n_channel = n_channel
        self.tnexts = [np.inf] * n_channel
        self.states = [0] * n_channel
            
    def outAct(self):
        super().outAct()
        currentChannels = self.findCurrChannels()
        
        for i in currentChannels:
            self.tnexts[i] = np.inf 
            self.states[i] = 0 

            if self.queue > 0:
                self.queue -= 1
                self.states[i] = 1
                self.tnexts[i] = self.tcurr + super().getDelay()
            elif self.nextElements is not None:
                next_element = np.random.choice(self.nextElements, p = self.p)
                next_element.inAct()

    def inAct(self):
        freeChannels = self.findEmptyChannels()
        for i in freeChannels:
            self.states[i] = 1 
            self.tnexts[i] = self.tcurr + super().getDelay()
            break
        else:
            if self.queue < self.max_queue:
                self.queue += 1
            else:
                self.failure += 1
        
    def displayInfo(self):
        super().displayInfo()
        print(f'failure = {self.failure}')
        
    def doStatistics(self, delta):
        self.meanQueue += delta * self.queue