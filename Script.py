
#University of British Columbia Department of Civil Engineering
#PGMatpMatching for ARCGIS
#---------------------------------------------------------------

import csv
from math import radians, cos, sin, asin, sqrt, acos
import numpy
from datetime import datetime
import csv
import itertools
import os
import arcpy
#from scipy import stats

#---------------------------------------------------------------

def readCSV(filename):
    #reads the data from a stored CSV file
    #the data pulls the GPS trace locations, as well as the placement in time
    #the timestamp will be used for temporal likelyhood
    #returns a list of the cleaned info from the csv
    
    #intial read of the csv
    with open (filename) as f:
        reader = csv.reader(f)
        next(reader)[6];
        rows = []
        for row in reader:
            rows.append(row)
    cleanedInfo = [];
    i = 0;

    #adds cleaned info
    #year, month, day, hour, minute, second, latitude, longitude 
    for info in rows:
        date = rows[i][0] + '-' + rows[i][1]+'-'+rows[i][2]+ ' '+rows[i][3]+':'+rows[i][4]+':' +rows[i][5]
        cleanedInfo.append([date,float(rows[i][5]),float(rows[i][6])]) #19 timestape in seconds, latt, long 
        i = i + 1;
    return cleanedInfo;

def distanceBetweenTwoPoints(pointOne,pointTwo):
    #usees the great circle formula to get the distance between two points
    #returns distance in km
    const_r = 6371 #radius in km
    lon1 = radians(pointOne[2]);
    lat1 = radians(pointOne[1]);
    lon2 = radians(pointTwo[2]);
    lat2 = radians(pointTwo[1]);


    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
    deltaSigma = acos( sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2) );
    return(deltaSigma * r);

def TimeDiff(date1, date2):
    #this method takes two times in order to get the time difference for the Temporal Likelihood
    #returns a rounded int

    fmt = '%Y-%m-%d %H:%M:%S'
    tstamp1 = datetime.strptime(date1, fmt)
    tstamp2 = datetime.strptime(date2, fmt)
    
    if tstamp1 > tstamp2:
        td = tstamp1 - tstamp2
    else:
        td = tstamp2 - tstamp1
    td_mins = int(round(td.total_seconds() / 60))
    return td_mins;

def GeoLikelihood(R,Z,sigma): #Normal dis
    #uses the formula in both papers
    #returns of a lisit of probabilites based on the distance to the edge
    # this is the most similar to our current approach

    normResults = []
    prob = [];
    holder = [0,R[1],R[2]];
    normInput= [];
    #gets the norm for every gps points relative to a point on a given route.
    for z in Z:
        normInput.append(distanceBetweenTwoPoints(z,holder));
    norm = numpy.linalg.norm(normInput, ord=1);
    normResults = [norm]

    #uses the Normal Function to get the probabilty for each gps point
    for i in normResults: #refers to equations 1 in Newson and Krumm
        e = 2.7182
        part1 = 1 / sqrt(2*3.1415926535*sigma);
        part2 = e**(-0.5*(i / sigma)**2);
        print((-0.5*(i / sigma)**2))
        prob.append(part1 * part2);
    return prob;             

def TopLikelihood(R,Z,sigma_t, populationmean,df):
    #uses t test to get probabilty of gps line segments and route segments 
    #returns a list of probabilities based on the gps points and the given route.
    
    prob = []
    holderlist = []

    for i in range(1,len(Z)):
        #This is the distance calculations
        norm1 = numpy.linalg.norm([Z[i][1],Z[i-1][1]],ord=1);
        norm2 = numpy.linalg.norm([Z[i][2],Z[i-1][2]],ord=1);
        totalNorm = norm1 + norm2;
        D = distanceBetweenTwoPoints(Z[i],Z[i-1]);  #normally would be based on the network distance, but this is based on c.
        holderlist.append(D);
        if D == 0: #this checks for null movement in two points to prevent a divid by zero error
            x = 0;
        else:
            x = max(0, totalNorm/D);
            n = len(Z); # sample size
            samplemean = sum(holderlist)/len(holderlist); #sample mean
            #t-test calculations
            t = (samplemean - populationmean)/(sigma_t / sqrt(n));
            dfdic = {0:.5, .687:.25,.860:.2, 1.064:.15, 1.325:.10, 1.725:.05, 2.086:.025, 2.528:.01, 2.845:.005} # the t table
            holder = dfdic.get(t); 
            if(holder == None):
                holder = .5;
            prob.append(holder);

    return prob;

def TemLikelihood(R,Z,speed,sigma):
    #Uses a normal distribution with a added constant  based on the speed of a the gps movement and a given speed limit
    #Returns a list of probabilties

    secondspeed = speed / 3600;
    prob = [];
    
    for i in range(1,len(Z)):
        x = distanceBetweenTwoPoints(Z[i],Z[i-1]);
        y = TimeDiff(Z[i][0],Z[i-1][0]);
        e = 2.71828
        part1 = 1 / sqrt(2*3.1415926535*sigma);
        part2 = e**(-0.5*((x/y) / sigma)**2);
        prob.append(part1 * part2);
    return(prob);

def combine(pg,pt,pr):
    #Used to combine the three likelihoods for a given route
    #Returns a single probalilty based on a given route.
    p = pg[0];
    holder = 1;
   
    #Geometric likelihood product
    for i in range(len(pg)):
        if ((pg[i] != None)):
            holder = holder * pg[i];
    
    #Topological likelihood product
    for i in range(len(pt)):
        if ((pt[i] != None)):
            holder = holder * pt[i];
    
    #Temporal likelihood product
    for i in range(len(pr)):
        if ((pr[i] != None)):
            holder = holder * pr[i];


    p = holder * p;
    return p;


#Reads parameters from ARCGIS
fileZ = arcpy.GetParameterAsText(0)
populationmean = float(arcpy.GetParameterAsText(1))
infc = arcpy.GetParameterAsText(2)
fc = arcpy.GetParameterAsText(3)

#reading the parameters from the .config file
configfileName =fileZ[0:fileZ.rindex("\\")] + "\\.config"
config = open(configfileName,"r")
holder = config.readline()
CONST_speed =  int(holder[holder.index(":")+1:holder.index("\n")])
holder = config.readline()
df = int(holder[holder.index(":")+1:holder.index("\n")])
if df == -1:
    df = len(Z) -1
holder = config.readline()
sigma_z = float(holder[holder.index(":")+1:holder.index("\n")])

#reads the route points for ARCGIS
routes = []
for row in arcpy.da.SearchCursor(infc, ["OID@", "SHAPE@"]):
    # Print the current polygon or polyline's ID
    print("Feature {}:".format(row[0]))
    partnum = 0

    # Step through each part of the feature
    for part in row[1]:
        route = []
        # Step through each vertex in the feature
        for pnt in part:
            if pnt:
                # Print x,y coordinates of current point
                print("{}, {}".format(pnt.X, pnt.Y))
                route.append(["",pnt.X,pnt.Y])
            routes.append(route)
            route = []

#Reads the route from arcgis
newZ = readCSV(fileZ); 
#Probability calculations
prob = []
pg = []
pt = []
pr = []
routeprob = []
routeholder =0;
for i in routes:
    for test in i:
        if len(test) == 3:
            pg = pg + GeoLikelihood(test,newZ,sigma_z);
            pt = pt + TopLikelihood(test,newZ,sigma_z,populationmean,df);
            pr = pr + TemLikelihood(test,newZ,CONST_speed,sigma_z);
    holder = combine(pg,pt,pr);
    prob.append(holder)
    for t in prob:
        routeholder = routeholder * t;
    routeprob.append(routeholder);
    routeholder = 0;

#selects = the best route
greatest = -1;
index = 0;
location = -1;
for i in routeprob:
    if i > greatest:
        greatest = i;
        location = index
    index = index +1;
if index == len(routeprob):
    index = index -1;
index = location
#adds the points to the selected route
cursor = arcpy.da.InsertCursor(fc, ["SHAPE@XY"])
for i in routes[index]:
    
    xy = (i[1], i[2])
    cursor.insertRow([xy])
