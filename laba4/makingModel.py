from generate import Generate
from model import Model
from process import Process
import random

def createSimple(n: int):
    c1 = Generate(delayMean=random.randint(1, 5), name='CREATOR', distribution='exp')
    pPrev = c1
    elements = [c1]
    for i in range(n - 1):
        p = Process(delayMean=random.randint(1, 5), distribution='exp')
        pPrev.nextElement = [p]
        elements.append(p)
        pPrev = p
    p = Process(nChannel=2, delayMean=random.randint(1, 5), distribution='exp')
    pPrev.nextElement = [p]
    elements.append(p)
    model = Model(elements)
    return c1, model

def createDifficult(n: int):
    c1 = Generate(delayMean=random.randint(1, 5), name='CREATOR', distribution='exp')
    pPrev = c1
    elements = [c1]
    for i in range(int(n / 5)):
        p = Process(delayMean=random.randint(1, 5), distribution='exp')
        pPrev.nextElement = [p]
        p1 = Process(delayMean=random.randint(1, 5), distribution='exp')
        p2 = Process(delayMean=random.randint(1, 5), distribution='exp')
        p.nextElement = [p1, p2]
        p.probability = [0.7, 0.3]
        if i != int(n / 5) - 1:
            p3 = Process(delayMean=random.randint(1, 5), distribution='exp')
            p1.nextElement = [p3]
            p2.nextElement = [p3]
            p4 = Process(delayMean=random.randint(1, 5), distribution='exp')
            p3.nextElement = [p4]
            pPrev = p4
            elements.append(p)
            elements.append(p1)
            elements.append(p2)
            elements.append(p3)
            elements.append(p4)
        else:
            p3 = Process(nChannel=2, delayMean=random.randint(1, 5), distribution='exp')
            p1.nextElement = [p3]
            p2.nextElement = [p3]
            elements.append(p)
            elements.append(p1)
            elements.append(p2)
            elements.append(p3)
            p3.channel = 2
    model = Model(elements)
    return c1, model
