#this is a single script for Dr.Fatmi
#this is to be able to run a python script in ArcGis with the given data
import csv
from math import radians, cos, sin, asin, sqrt
CONST_speed = 50; #50 km assumption
R = []; #Road Vectors
Z = []; #GPS point
def readCSV(filename):
    with open ("data.csv") as f:
        reader = csv.reader(f)
        next(reader)[18];
        rows = []
        for row in reader:
            rows.append(row)
    cleanedInfo = [];
    i = 0;
    for info in rows:
        cleanedInfo.append([rows[i][18],rows[i][8],rows[i][7]]) #19 speed_km, latt, long 
        i = i + 1;
    return cleanedInfo;
def distanceBetweenTwoPoints(pointOne,pointTwo):
    const_r = 6371 #radius in km
    lon1 = radians(pointOne[2]);
    lat1 = radians(pointOne[1]);
    lon2 = radians(pointTwo[2]);
    lat2 = radians(pointTwo[1]);
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    return(c * r)

