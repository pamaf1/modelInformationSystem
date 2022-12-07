from Element import Element


class Create(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def outAct(self):
        super().outAct()
        self.tnexts[0] = self.tcurr + super().getDelay()
        nextElement1 = self.nextElements[0]
        nextElement2 = self.nextElements[1]
        if nextElement1.queue == nextElement2.queue:
            nextElement1.inAct()
        elif nextElement1.queue < nextElement2.queue:
            nextElement1.inAct()
        else:
            nextElement2.inAct()