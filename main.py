import datetime
from data.generator import fullDataSet, saveDataSet

def main():
    input, output = fullDataSet("./datasets/raw/logs_WT.csv", "./datasets/raw/Resultaten_WT.csv", None, datetime.datetime(2021, 2, 10, 0, 0).timestamp())
    saveDataSet(input, output, "./datasets")


if __name__ == "__main__":
    main()
