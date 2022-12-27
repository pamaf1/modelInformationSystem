import numpy as np
from Element import Element


class Create(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def outAct(self):
        super().outAct() 
        self.tnexts[0] = self.tcurr + super().getDelay()
        next_element = np.random.choice(self.nextElements, p=self.p)
        next_element.inAct()