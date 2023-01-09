import numpy as np
from element import Element

class Process(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tNext = [np.inf] * self.channel
        self.state = [0] * self.channel

    def inAct(self):
        freeRoute = self.freeChannel()
        if len(freeRoute) > 0:
            for i in freeRoute:
                self.state[i] = 1
                self.tNext[i] = self.tCurrent + super().getDelay()
                break
        else:
            if self.queue < self.maxQueue:
                self.queue += 1
            else:
                self.failure += 1

    def outAct(self):
        currentChannel = self.currentChannel()
        for i in currentChannel:
            super().outAct()
            self.tNext[i] = np.inf
            self.state[i] = 0
            if self.queue > 0:
                self.queue -= 1
                self.state[i] = 1
                self.tNext[i] = self.tCurrent + self.getDelay()
            if self.nextElement is not None:
                nextElement = self.chooseNextElement()
                nextElement.inAct()
