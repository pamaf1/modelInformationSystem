import numpy as np
from Element import Element


class Create(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def outAct(self):
        super().outAct()
        self.tnexts[0] = self.tcurr + super().getDelay()
        self.nextPatientType = np.random.choice([1, 2, 3], p = [.5, .1, .4])
        self.nextElement = np.random.choice(self.nextElements, p=self.p)
        self.nextElement.inAct(self.nextPatientType, self.tcurr)