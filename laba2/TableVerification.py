import pandas as pd
from Model import Model
from Create import Create
from Process import Process
from Despose import Despose
from Element import Element
from IPython.display import clear_output

nParam = 5
maxQlist = [5] * nParam + [7] * nParam + [9] * nParam
creationDelayList = [1] * nParam + [3] * nParam + [5] * nParam
processDelayList = [1] * nParam + [3] * nParam + [5] * nParam
timeModelingList = [i * 100 for i in range(1, nParam + 1)] + [i * 100 for i in range(1, nParam + 1)] + [i * 100 for i in range(1, nParam + 1)]

rows = []
df = pd.DataFrame()

for i in range(nParam * 3):
    Element.id = 0
    c = Create(delayMean = creationDelayList[i], name = 'CREATOR', distribution = 'exp')
    p = Process(maxqueue = maxQlist[i], delayMean = processDelayList[i], name = 'PROCESSOR 1', distribution = 'exp')
    p2 = Process(maxqueue = maxQlist[i], delayMean = processDelayList[i], name = 'PROCESSOR 2', distribution = 'exp')
    p3 = Process(maxqueue = maxQlist[i], delayMean = processDelayList[i], name = 'PROCESSOR 3', distribution = 'exp')
    d = Despose(delayMean = processDelayList[i], name = 'DESPOSER')
    
    c.nextElements = [p]
    p.nextElements = [p2]
    p2.nextElements = [p3]
    p3.nextElements = [d]
    
    c.p = [1]
    p.p = [1]
    p2.p = [1]
    p3.p = [1]
    
    elements = [c, p, p2, p3, d]

    model = Model(elements, displayLogs = False)
    simulation_result = model.simulation(timeModelingList[i])
    param = { 'delay mean create': creationDelayList[i],
              'delay process create': processDelayList[i],
              'distribution': 'exp',
              'maxqueue': maxQlist[i],
              'timeModeling': timeModelingList[i] }
    rows.append( {**param, **simulation_result} )

df = df.append(rows)
clear_output()
with pd.option_context('display.max_rows', 10):
    print(df.to_string())