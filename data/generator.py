from csv import writer
import random

from data.parser import parse

def generateDataSet(logsPath: str, resultsPath: str, startDate: float, stopDate: float, amount = 10):
    logs, results = parse(logsPath, resultsPath)
    
    inputSet = []
    outputSet = []
    
    for id, result in results:
        actions = getActions(id, logs)
        entries = randomentries(amount, actions, startDate, stopDate)
        resultCategory = 0
        if result >= 8 and result <= 12:
            resultCategory = 1
        elif result > 12:
            resultCategory = 2
        
        for entry in entries:
            inputSet.append(entry)
            
            
            outputSet.append([resultCategory])
            
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

    inputSet = []
    outputSet = []

    for id, result in results:
        inEntry = [0, 0, 0, 0, 0]
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

def getActions(id, logs):
    return list(filter(lambda x: x[0] == id, logs))

def fractionToTime(fraction: float, start: float, stop: float) -> float:
    return (fraction * (stop - start)) + start

def timeToFraction(time: float, start: float, stop: float) -> float:
    return (time - start) / (stop - start)
