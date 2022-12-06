import numpy as np
from FunRand import FunRand


class Element:
    id = 0
    def __init__(self, name = None, delayMean = 1., delay_dev = 0., distribution = '', p = None, n_channel = 1):
        self.p = p
        self.id = Element.id
        Element.id += 1
        self.name = f'element_{self.id}' if name is None else name
        self.delayMean = delayMean
        self.delay_dev = delay_dev 
        self.distribution = distribution
        self.quantity = 0
        self.tcurr = 0 
        self.nextElements = None
        self.n_channel = n_channel
        self.tnexts = [0.0] * self.n_channel
        self.states = [0] * self.n_channel
        
    def getDelay(self):
        if self.distribution == 'exp':
            return FunRand.exp(self.delayMean)
        elif self.distribution == 'unif':
            return FunRand.unif(self.delayMean, self.delay_dev)
        elif self.distribution == 'norm':
            return FunRand.norm(self.delayMean, self.delay_dev)
        else:
            return self.delayMean
    
    def outAct(self):
        self.quantity += 1
        
    def showStatistic(self):
        print(f'{self.name}: Quantity = {self.quantity}, State={self.states}')

    def displayInfo(self):
        print(f'{self.name}: Quantity = {self.quantity}, State = {self.states}, tnext = {np.round(self.tnexts, 9)}')

    def findCurrChannels(self):
        res = []
        for i in range(self.n_channel):
            if self.tnexts[i] == self.tcurr:
                res.append(i)
        return res
    
    def findEmptyChannels(self):
        empty_channels = []
        for i in range(self.n_channel):
            if self.states[i] == 0:
                empty_channels.append(i)
        return empty_channels