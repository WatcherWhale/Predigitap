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

            ts=int(row[17])
            date=datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            logs.append([int(float(row[12])),category,date])

    return logs

def parse_results(resultpath):
    with open(resultpath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        results=[]
        next(reader, None)

        for row in reader:
            points=row[3]
            deelgenomen=row[5]
            points=int(float(points.replace(',','.')))
            if (deelgenomen==''):
                results.append([int(row[0]),points])
    return results


def merge_var(action,resource):
    if(action=='updated'):
        return 'comletion'
    if (action=='downloaded'):
        return 'downloaded'
    if (action=='viewed'and resource=='course'):
        return 'course'
    if (action=='viewed'and resource=='course_module'):
        return 'course_module'
    if (action=='viewed'and resource=='discussion'):
        return 'discussion'
    return None

if __name__ == '__main__':
    parse("data/logs_WT.csv","data/Resultaten_WT.csv")