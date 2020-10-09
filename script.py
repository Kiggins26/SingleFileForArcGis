#this is a single script for Dr.Fatmi
#this is to be able to run a python script in ArcGis with the given data
import csv
from math import radians, cos, sin, asin, sqrt
from scipy import stats, sparse
import numpy
def readCSV(filename):
    with open (filename) as f:
        reader = csv.reader(f)
        next(reader)[18];
        rows = []
        for row in reader:
            rows.append(row)
    cleanedInfo = [];
    i = 0;
    for info in rows:
        cleanedInfo.append([(60*60*rows[i][3]+60*rows[i][4]+rows[i][5]),rows[i][8],rows[i][7]]) #19 speed_km, latt, long 
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
            holder.append(sqrt(z[1]**2 + z[2]**2));
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

def TopLikelihood(R,Z,sigma_t, populationmean): #Students’ t-distribution with 20 degrees of freedom
    prob = []
    for i in range(1,len(Z)):
        norm1 = numpy.linalg.norm([Z[i][1],Z[i-1][1]],ord=1);
        norm2 = numpy.linalg.norm([Z[i][2],Z[i-1][2]],ord=1);
        totalNorm = norm1 + norm2;
        D = distanceBetweenTwoPoints(Z[i],Z[i-z]);  #normally would be based on the network distance, but this is based on c.
        x = max(0, totalNorm/D);
        n = len(Z); # sample size
        df = 20; #degrees of freedom says to use 20 in the paper
        samplemean = 0; #sample mean
        t = (samplemean - populationmean)/(sigma_t / sqrt(n));
        #insert dic here
        holder = 0;
        prob.append(holder);
    return prob;

def TemLikelihood(R,Z,speed,sigma): #Expontial dis
   secondspeed = speed / 3600;
   prob = [];
   for i in range(1,len(Z)):
       x = distanceBetweenTwoPoints(Z[i],Z[i-1]);
       y = Z[i][0] - Z[i-1][0];
       e = 2.71828
       part1 = 1 / sqrt(2*3.1415926535*sigma);
       part2 = e**(-0.5*((x/y) / sigma)**2);
       prob.append(part1 * part2);
    return(prob);

def combine(pg,pt,pr):
    p = 0;
    return p;

CONST_speed = 50; #50 km assumption
R = []; #Road Vectors, made of the midpoints on the map, so the more work is needed to be optimal.
Z = readCSV("data.csv"); #GPS point
sigma_z = 4.07 # meters based on the paper data, but can be calcuted by 1.4826 median(||zt-xti|| great circle)
populationmean = 2134;
