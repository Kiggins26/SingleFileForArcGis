#this is a single script for Dr.Fatmi
#this is to be able to run a python script in ArcGis with the given data
import csv
def readCSV(filename):
    with open (data.csv) as f:
        reader = csv.reader(f)
        next(reader)
        rows = []
        for row in reader:
            rows.append(row)
    return rows

print(readCSV("data.csv"))
`
