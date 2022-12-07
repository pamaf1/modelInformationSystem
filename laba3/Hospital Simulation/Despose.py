import numpy as np
from Element import Element


class Despose(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tnexts = [np.inf]

        self.finishTime1Delta = 0
        self.finishTime2Delta = 0
        self.finishTime3Delta = 0
        self.nType1 = 0
        self.nType2 = 0
        self.nType3 = 0

    def outAct(self, *args):
        pass
        
    def inAct(self, nextPatientType, startTime):
        if nextPatientType == 1:
            self.nType1 += 1
            self.finishTime1Delta += self.tcurr - startTime
        elif nextPatientType == 2:
            self.nType2 += 1
            self.finishTime2Delta += self.tcurr - startTime
        elif nextPatientType == 3:
            self.nType3 += 1
            self.finishTime3Delta += self.tcurr - startTime
        super().outAct()