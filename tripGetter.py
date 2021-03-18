import os
import arcpy

CSV = arcpy.GetParameterAsText(0)
tripid= arcpy.GetParameterAsText(1)
fcout = arcpy.GetParameterAsText(2)

tripPoints = []
reader = open(str(CSV),"r")
row = reader.readline()
while(row):
    if tripid in row:
        holder = row.split(",")
        if tripid in holder[0]:
            tripPoints.append((holder[1],holder[2]))
    row = reader.readline()
    
if not tripPoints:
    arcpy.AddMessage("No trip id found")
else:
    with arcpy.da.InsertCursor(fcout, ['SHAPE@']) as cursor:
            cursor.insertRow([tripPoints])
