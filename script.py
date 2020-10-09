#this is a single script for Dr.Fatmi
#this is to be able to run a python script in ArcGis with the given data
import csv
from math import radians, cos, sin, asin, sqrt
from scipy import stats, sparse
import numpy
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

def GeoLikelihood(R,Z,sigma): #Normal dis
    smallestDistance = []
    normResults = []
    holder = [];
    for z in Z:
        for r in R:
            holder.append(z);
        norm = numpy.linalg.norm(holder - r, ord=1);
        normResults.append(norm);
        holder.clear();
    prob = [];
    for i in normResults: #refers to equations 1 in Newson and Krumm
        e = 2.71828
        part1 = 1 / sqrt(2*3.1415926535*sigma);
        part2 = e**(-0.5*(i / sigma)**2);
        prob.append(part1 * part2);
    return prob;             

def TopLikelihood(R,Z): #Students’ t-distribution with 20 degrees of freedom
    for z in Z:
        for r in R:
            holder = 0;
            max(0,holder - 1);

def TemLikelihood(R,Z,speed): #Expontial dis
    for z = Z:
        for r in R:

def combine(pg,pt,pr):
    p = 0;
    return p;

CONST_speed = 50; #50 km assumption
R = []; #Road Vectors, made of the midpoints on the map, so the more work is needed to be optimal.
Z = []; #GPS point
sigma_z = 4.07 # meters based on the paper data, but can be calcuted by 1.4826 median(||zt-xti|| great circle)

