from csv import writer
import random
import numpy as np

from data.parser import parse, get_eventnames, get_neg_events

def generateDataSetZ(logsPath: str, resultsPath: str, startDate: float, stopDate: float, amount = 10) -> (list, list):
    logs, results = parse(logsPath, resultsPath)

    inputSet = []
    outputSet = []

    results_r = np.array(results)[:,1]
    cats_r = resultToCategory(results_r)

    mean = np.mean(cats_r)
    std = np.std(cats_r)


    for id, result in results:
        if result < 1:
            continue
        actions = getActions(id, logs)
        entries = randomentries(amount, actions, startDate, stopDate)

        result_z = (resultToCategory(result) - mean) / std
        for entry in entries:
            inputSet.append(entry)

            outputSet.append([result_z])

    return inputSet, outputSet, mean, std

def generateDataSetCat(logsPath: str, resultsPath: str, startDate: float, stopDate: float, amount = 10, skipZero = False) -> (list, list):
    logs, results = parse(logsPath, resultsPath)

    inputSet = []
    outputSet = []

    for id, result in results:
        if result < 1 and skipZero:
            continue
        actions = getActions(id, logs)
        entries = randomentries(amount, actions, startDate, stopDate)

        result = resultToCategory(result) - 1
        for entry in entries:
            inputSet.append(entry)

            outputSet.append([result])

    return inputSet, outputSet

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

def constantDataSet(logsPath: str, resultsPath: str, startDate: float, stopDate: float, fraction = 0.3):
    logs, results = parse(logsPath, resultsPath)

    inputSet = []
    outputSet = []

    for id, result in results:
        if result < 1:
            continue
        actions = getActions(id, logs)
        entries = constantentries(actions, startDate, stopDate, fraction)

        result = resultToCategory(result) - 1
        for entry in entries:
            inputSet.append(entry)

            outputSet.append([result])

    return inputSet, outputSet

def constantentries(actions, start: float, stop: float, fraction: float):
    entries = []
    names = get_eventnames()
    
    inEntry = np.zeros(len(names))

    for id, category, time in actions:
        timeFraction = timeToFraction(time, start, stop)
        if timeFraction > fraction:
            continue
        inEntry[int(category)] += 1

    entries.append(inEntry)

    return entries

def randomentries(amount, actions, start: float, stop: float):
    entries = []
    names = get_eventnames()
    
    for _ in range(amount):
        fraction = random.random()

        inEntry = np.zeros(len(names) + 1)
        inEntry[len(inEntry) - 1] = fraction

        for id, category, time in actions:
            timeFraction = timeToFraction(time, start, stop)
            if timeFraction > fraction:
                continue
            inEntry[int(category)] += 1

        entries.append(inEntry)

    return entries

def timedEntries(amount, actions, start: float, stop: float):
    entries = []
    names = get_eventnames()
    
    for i in range(amount + 1):
        fraction = i/amount
        inEntry = np.zeros(len(names) + 1)
        inEntry[len(names)] = fraction

        for id, category, time in actions:
            timeFraction = timeToFraction(time, start, stop)
            if timeFraction > fraction:
                continue
            inEntry[int(category)] += 1

        entries.append(inEntry)

    return entries

def fullDataSet(logsPath: str, resultsPath: str, startDate: float, stopDate: float):
    logs, results = parse(logsPath, resultsPath)

    names = get_eventnames()
    names.append("results")
    inputSet = [names]
    outputSet = []

    for id, result in results:
        inEntry = np.zeros(len(names))
        inEntry[len(inEntry) - 1] = result
        for id, category, time in getActions(id, logs):
            if time > stopDate:
                continue
            inEntry[int(category)] += 1

        outputSet.append([result])
        inputSet.append(inEntry)

    return inputSet, outputSet

def fullDataSetAll(logsPath: str, resultsPath: str, startDate: float, stopDate: float):
    logs, results = parse(logsPath, resultsPath)

    names= get_neg_events()
    names.append("results")
    inputSet = [names]
    outputSet = []

    for id, result in results:
        inEntry = [0 for _ in range(len(names) + 1 ) ]
        inEntry[len(inEntry) - 1] = result
        for id, category, time in getActions(id, logs):
            if time > stopDate:
                continue
            inEntry[int(category)] += 1

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
    return np.array(list(filter(lambda x: x[0] == id, logs)))

def fractionToTime(fraction: float, start: float, stop: float) -> float:
    return (fraction * (stop - start)) + start

def timeToFraction(time: float, start: float, stop: float) -> float:
    return (time - start) / (stop - start)

def resultToCategory(r):
    return np.where(r < 8, 1, 0) + np.where((r >= 8) & (r <= 12), 2, 0) + np.where(r > 12, 3, 0)


def cathegoryfunction(logsPath: str, resultsPath: str, amount = 10) -> (list, list):
    logs, results = parse(logsPath, resultsPath)

    result_r= np.array(results)[:,1]

    result_cat=[]
    test=resultToCategory(result_r)
    for i in range(len(test)):
        result = [0, 0, 0]

        if test[i] == 1:
            result[0] += 1
        elif test[i] == 2:
            result[1] += 1
        elif test[i] == 3:
            result[2] += 1

        result_cat.append(result)

        #result[int(resultToCategory(result_r))] = 1
    return result_cat

