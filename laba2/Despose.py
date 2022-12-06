import numpy as np
from Element import Element


class Despose(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tnexts = [np.inf]

    def inAct(self):
        super().outAct()