import os
import arcpy

CSV = arcpy.GetParameterAsText(0)
tripid= float(arcpy.GetParameterAsText(1))
fcout = arcpy.GetParameterAsText(2)

tripPoints = []
reader = open(str(CSV),"r")
row = reader.readline()
while(row):
    if tripid in row:
        holder = row.split(",")
        tripPoints.append()
    row = reader.readline((holder[1],holder[2]))
with arcpy.da.InsertCursor(fcout, ['SHAPE@']) as cursor:
        cursor.insertRow([tripPoints])


