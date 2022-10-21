import csv
from datetime import datetime

def parse(logspath, resultpath):
    logs = parse_logs(logspath)
    results=parse_results(resultpath)
    return logs, results

def parse_logs(logspath):
    with open(logspath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader, None)
        logs=[]

        for row in reader:
            category=merge_var(row[3],row[4])

            if (category is None):
                continue

            logs.append([int(float(row[12])), category, float(row[17])])

    return logs

def parse_results(resultpath):
    with open(resultpath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        results=[]
        next(reader, None)

        for row in reader:
            points=row[3]
            deelgenomen1 = row[2]
            deelgenomen2 = row[5]
            points=int(float(points.replace(',','.')))

            if (deelgenomen1 == "" and deelgenomen2 == ""):
                results.append([int(row[0]), points])

    return results

def merge_var(action) -> int:
    action=action.lstrip("\\")
    action=action.replace("\\","_")

    eventname=[]
    with open('./datasets/eventnames.txt', 'r') as file:
      for line in file:
        eventname.append(line.strip())
    try:
      return eventname.index(action)
    except ValueError:
        return None
