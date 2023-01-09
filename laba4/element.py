import FunRand as ran
from copy import deepcopy
import numpy as np

class Element:
    nextId = 0
    def __init__(self, name=None, delayMean=1., delayDev=0., distribution='', probability=1, nChannel=1,
        maxQueue=float('inf')):
        self.tNext = [0] * nChannel
        self.delayMean = delayMean
        self.delayDev = delayDev
        self.quantity = 0
        self.tCurrent = 0
        self.state = [0] * nChannel
        self.nextElement = None
        self.idElem = Element.nextId
        self.distribution = distribution
        self.probability = [probability]
        self.priority = [1]
        self.queue = 0
        self.maxObservedQueue = 0
        self.maxQueue = maxQueue
        self.channel = nChannel
        self.failure = 0
        Element.nextId += 1
        self.name = f'Element_{self.idElem}' if name is None else name


    def chooseNextElement(self):
        if self.probability != [1] and self.priority != [1]:
            raise Exception('Route selection is ambiguous: probability and priority are set simultaneously')
        elif self.probability != [1]:
            nextElement = np.random.choice(a=self.nextElement, p=self.probability)
            return nextElement
        elif self.priority != [1]:
            nextElement = self.chooseByPriority()
            return nextElement
        elif self.probability == [1] and self.priority == [1]:
            return self.nextElement[0]

    def chooseByPriority(self):
        priorities = deepcopy(self.priority)
        minQueue = float('inf')
        minQueueIndex = 0

        for p in range(len(priorities)):
            if min(priorities) == 100000:
                break
            maxPriorIndex = priorities.index(min(priorities))
            if 0 in self.nextElement[maxPriorIndex].state:
                return self.nextElement[maxPriorIndex]
            else:
                if self.nextElement[maxPriorIndex].queue < minQueue:
                    minQueue = self.nextElement[maxPriorIndex].queue
                    minQueueIndex = self.nextElement.index(self.nextElement[maxPriorIndex])
            priorities[maxPriorIndex] = 100000
        return self.nextElement[minQueueIndex]

    def getDelay(self):
        if 'exp' == self.distribution:
            return ran.exp(self.delayMean)
        elif 'norm' == self.distribution:
            return ran.norm(self.delayMean, self.delayDev)
        elif 'uniform' == self.distribution:
            return ran.uniform(self.delayMean, self.delayDev)
        else:
            return self.delayMean

    def inAct(self):
        pass

    def getState(self):
        return self.state

    def setState(self, newState):
        self.state = newState

    def setTNext(self, tNextNew):
        self.tNext = tNextNew

    def getTCurr(self):
        return self.tCurrent

    def outAct(self):
        self.quantity += 1

    def result(self):
        print(f'{self.name} quantity = {str(self.quantity)} state = {self.state}')

    def showInfo(self):
        print(f'{self.name} state = {self.state} quantity = {self.quantity} tNext = {self.tNext}')

    def freeChannel(self):
        freeChannels = []
        for i in range(self.channel):
            if self.state[i] == 0:
                freeChannels.append(i)
        return freeChannels

    def currentChannel(self):
        currentChannels = []
        for i in range(self.channel):
            if self.tNext[i] == self.tCurrent:
                currentChannels.append(i)
        return currentChannels
