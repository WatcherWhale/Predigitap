from csv import writer
import random
import numpy as np

from data.parser import parse

def generateDataSet(logsPath: str, resultsPath: str, startDate: float, stopDate: float, amount = 10) -> (list, list):
    logs, results = parse(logsPath, resultsPath)

    inputSet = []
    outputSet = []
    
    results_r = np.array(results)[:,1]
    cats_r = resultToCategory(results_r)
    
    mean = np.mean(cats_r)
    std = np.std(cats_r)

    for id, result in results:
        actions = getActions(id, logs)
        entries = randomentries(amount, actions, startDate, stopDate)
        
        result_z = (resultToCategory(result) - mean) / std

        for entry in entries:
            inputSet.append(entry)

            outputSet.append([result_z])

    return inputSet, outputSet, mean, std

def timedDataSet(logsPath: str, resultsPath: str, startDate: float, stopDate: float, amount = 10):
    logs, results = parse(logsPath, resultsPath)

    inputSet = [[] for _ in range(amount + 1)]
    outputSet = [[] for _ in range(amount + 1)]

    for id, result in results:
        actions = getActions(id, logs)
        entries = timedEntries(amount, actions, startDate, stopDate)
        resultCategory = 0
        if result >= 8 and result <= 12:
            resultCategory = 1
        elif result > 12:
            resultCategory = 2

        for i in range(amount + 1):
            inputSet[i].append(entries[i])
            outputSet[i].append([resultCategory])

    return inputSet, outputSet

def randomentries(amount, actions, start: float, stop: float):
    entries = []
    for _ in range(amount):
        fraction = random.random()
        inEntry = [0, 0, 0, 0, 0, fraction]

        for id, category, time in actions:
            timeFraction = timeToFraction(time, start, stop)
            if timeFraction > fraction:
                continue
            inEntry[category] += 1

        entries.append(inEntry)

    return entries

def timedEntries(amount, actions, start: float, stop: float):
    entries = []
    for i in range(amount + 1):
        fraction = i/amount
        inEntry = [0, 0, 0, 0, 0, fraction]

        for id, category, time in actions:
            timeFraction = timeToFraction(time, start, stop)
            if timeFraction > fraction:
                continue
            inEntry[category] += 1

        entries.append(inEntry)

    return entries

def fullDataSet(logsPath: str, resultsPath: str, startDate: float, stopDate: float):
    logs, results = parse(logsPath, resultsPath)

    inputSet = [["completion", "downloaded", "course", "course_module", "discussion", "result"]]
    outputSet = []

    for id, result in results:
        inEntry = [0, 0, 0, 0, 0, result]
        for id, category, time in getActions(id, logs):
            if time > stopDate:
                continue
            inEntry[category] += 1

        outputSet.append([result])
        inputSet.append(inEntry)

    return inputSet, outputSet

def saveDataSet(inputSet, outputSet, directoryPath):
    with open(directoryPath + "/input.csv", "w+") as input_csv:
        cw = writer(input_csv, delimiter=';')
        cw.writerows(inputSet)

    with open(directoryPath + "/output.csv", "w+") as input_csv:
        cw = writer(input_csv, delimiter=';')
        cw.writerows(outputSet)

def loadDataSet(inputPath, outputPath):
    pass

def getActions(id, logs):
    return list(filter(lambda x: x[0] == id, logs))

def fractionToTime(fraction: float, start: float, stop: float) -> float:
    return (fraction * (stop - start)) + start

def timeToFraction(time: float, start: float, stop: float) -> float:
    return (time - start) / (stop - start)

def resultToCategory(r):
    return np.where(r < 8, 1, 0) + np.where((r >= 8) & (r <= 12), 2, 0) + np.where(r > 12, 3, 0)