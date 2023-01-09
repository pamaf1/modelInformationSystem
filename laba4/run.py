import time
from element import Element
from model import Model
import makingModel
import matplotlib.pyplot as plt

def calculateTheoretical(create: Element, model: Model, modelingTime: int):
    basicValue = 1 / create.delayMean
    countAccumulate = 0
    for i in range(len(model.list) - 1):
        if bool(model.list[i].nextElement) or model.list[i].nextElement is None:
            if model.list[i].nextElement is None or not len(model.list[i].nextElement) >= 2:
                countAccumulate += 1
    return (2 * basicValue + basicValue * countAccumulate) * 2 * modelingTime

def analyze(func):
    modelingTime = 10000
    timeTesting = 3
    elementsTesting = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    analyticTime = []
    theoreticalOperationCount = []
    for i in elementsTesting:
        analyticTimeAccumulator = 0
        theoreticalOperationCountAccumulator = 0
        for j in range(timeTesting):
            c1, model = func(i)
            theoreticalOperationCountAccumulator += calculateTheoretical(c1, model, modelingTime)
            start = time.perf_counter()
            model.simulating(modelingTime)
            end = time.perf_counter()
            analyticTimeAccumulator += end - start
        analyticTime.append(analyticTimeAccumulator / timeTesting)
        theoreticalOperationCount.append(theoreticalOperationCountAccumulator / timeTesting)
    plt.title("Аналітична оцінка")
    plt.xlabel("Складність моделі")
    plt.ylabel("Час")
    plt.plot(elementsTesting, analyticTime, color="blue")
    plt.show()
    plt.title("Теоретична оцінка")
    plt.xlabel("Складність моделі")
    plt.ylabel("Операції")
    plt.plot(elementsTesting, theoreticalOperationCount, color="red")
    plt.show()

def run():
    analyze(makingModel.createSimple)
    # analyze(makingModel.createDifficult)

run()