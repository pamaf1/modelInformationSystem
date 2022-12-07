import numpy as np
from FunRand import FunRand


class Element:
    id = 0
    def __init__(self, name = None, delayMean = 1., delayDev = 0., distribution = '', p = None, nChannel = 1):
        self.distribution = distribution
        self.nextElements = None
        self.nChannel = nChannel
        self.tnexts = [0.0] * self.nChannel
        self.states = [0] * self.nChannel
        self.delayMean = delayMean
        self.delayDev = delayDev
        self.quantity = 0
        self.tcurr = 0
        self.p = p
        self.id = Element.id
        Element.id += 1
        self.name = f'element_{self.id}' if name is None else name

        
    def getDelay(self):
        if self.distribution == 'exp':
            return FunRand.exp(self.delayMean)
        elif self.distribution == 'unif':
            return FunRand.unif(self.delayMean, self.delayDev)
        elif self.distribution == 'norm':
            return FunRand.norm(self.delayMean, self.delayDev)
        elif self.distribution == 'erlanga':
            return FunRand.erlanga(self.delayMean, self.delayDev)
        else:
            return self.delayMean
        
    def inAct(self):
        pass
    
    def outAct(self):
        self.quantity += 1
        
    def displayStatistic(self):
        print(f'{self.name}: Quantity = {self.quantity}, State = {self.states};')

    def displayInfo(self):
        print(f'{self.name}: Quantity={self.quantity}, State={self.states}, tnext={np.round(self.tnexts, 9)}')
        
    def CurrentChannels(self):
        currentChannels = []
        for i in range(self.nChannel):
            if self.tnexts[i] == self.tcurr:
                currentChannels.append(i)
        return currentChannels
    
    def EmptyChannels(self):
        emptyChannels = []
        for i in range(self.nChannel):
            if self.states[i] == 0:
                emptyChannels.append(i)
        return emptyChannels

    def showStatistics(self, delta):
        pass