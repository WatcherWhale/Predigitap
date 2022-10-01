import csv
import json

from datetime import datetime

def parse(logspath, resultpath):
    logs = parse_logs(logspath)
    results=parse_results(resultpath)
    return logs, results

def parse_logs(logspath):
    with open(logspath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        header_row = next(reader, None)

        userid_col = header_row.index("userid")
        action_col = header_row.index("eventname")
        target_col = header_row.index("target")
        time_col = header_row.index("timecreated")

        logs=[]

        for row in reader:
            category = merge_var(row[action_col])

            if (category is None):
                continue

            logs.append([int(float(row[userid_col])), category, float(row[time_col])])

    return logs

def parse_logs_all(logspath):
    with open(logspath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        header_row = next(reader, None)

        userid_col = header_row.index("userid")
        action_col = header_row.index("eventname")
        target_col = header_row.index("target")
        time_col = header_row.index("timecreated")

        logs=[]
        
        events = get_neg_events()

        for row in reader:
            
            if merge_var(row["action_col"]) is not None:
                continue
            
            index = events.index(row["action_col"])
            
            logs.append([int(float(row[userid_col])), index, float(row[time_col])])

    return logs

def parse_results(resultpath):
    with open(resultpath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')

        results=[]

        header_row = next(reader, None)

        id_col = header_row.index("id")
        result_col = header_row.index("Numerische quotering 1")
        absentcode1_col = header_row.index("Ingevoerde afwezigheidscode 1")
        absentcode2_col = header_row.index("Ingevoerde afwezigheidscode 2")
        result_view_1_col = header_row.index("Weergave deliberatieresultaat 1")

        for row in reader:
            try:
                points = row[result_col]
                if points == "":
                    points = "0.0"
                points = int(float(points.replace(',','.')))

                deelgenomen1 = row[absentcode1_col]
                deelgenomen2 = row[absentcode2_col]
                deelgenomen3 = row[result_view_1_col]

                if (deelgenomen1 == "" and deelgenomen2 == "" and deelgenomen3 != "[V]"):
                    results.append([int(row[id_col]), points])
            except:
                print(row[id_col], "has been skipped due to parsing errors.")
                print(row[result_col])
                print(row[absentcode1_col])
                print(row[absentcode2_col])

    return results

def merge_var(action) -> int:
    action=action.lstrip("\\")
    action=action.replace("\\","_")
    
    events = get_events()
    names = get_eventnames()
    for key in names:
        if action in events[key]:
            return names.index(key)

def get_eventnames():
    return list(get_events().keys())
    
def get_events():
    with open("data/events.json") as file:
        return json.load(file)
    
def get_neg_events():
    with open("./datasets/raw/eventnames.txt") as eventsFile:
        events = eventsFile.readlines()
    
    neg_events = []
    
    for event in events:
        if merge_var(event.strip()) is None:
            neg_events.append(event)
    
    print(len(neg_events))
    
    return neg_events