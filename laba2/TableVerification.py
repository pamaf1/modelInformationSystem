import pandas as pd
from Model import Model
from Create import Create
from Process import Process
from Element import Element
from IPython.display import clear_output

nParam = 10
maxQlist = [3] * nParam + [5] * nParam
creationDelayList = [1] * nParam + [1] * nParam
processDelayList = [1] * nParam + [1] * nParam
timeModelingList = [i * 100 for i in range(1, nParam + 1)] + [i * 100 for i in range(1, nParam + 1)]

rows = []
df = pd.DataFrame()

for i in range(nParam * 2):
    Element.id = 0
    c = Create(delayMean = creationDelayList[i], name = 'CREATOR', distribution = 'exp')
    p = Process(maxqueue = maxQlist[i], delayMean = processDelayList[i], name = 'PROCESSOR', distribution = 'exp')
    c.nextElements = [p]
    elements = [c, p]
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