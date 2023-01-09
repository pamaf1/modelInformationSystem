from element import Element

class Generate(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def outAct(self):
        super().outAct()
        self.tNext[0] = self.tCurrent + super().getDelay()
        nextElement = self.chooseNextElement()
        nextElement.inAct()
