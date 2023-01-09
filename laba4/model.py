import numpy as np
from element import Element

class Model:
    def __init__(self, elements: list[Element]):
        self.list = elements
        self.event = 0
        self.tNext = 0.0
        self.tCurrent = self.tNext

    def simulating(self, time):
        while self.tCurrent < time:
            self.tNext = float('inf')
            for e in self.list:
                tNextVal = np.min(e.tNext)
                if tNextVal < self.tNext:
                    self.tNext = tNextVal
                    self.event = e.idElem
            self.tCurrent = self.tNext
            for e in self.list:
                e.tCurrent = self.tCurrent
            if len(self.list) > self.event:
                self.list[self.event].outAct()
            for e in self.list:
                if self.tCurrent in e.tNext:
                    e.outAct()
