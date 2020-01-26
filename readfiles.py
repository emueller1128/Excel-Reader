#Import modules, set workspace
import arcpy, xlrd
arcpy.env.workspace = "C:/GIS_Programming/Final_Exam_Data"
arcpy.env.overwriteOutput = True

#Create new file geodatabase 
gdb_path = "C:/GIS_Programming/Final_Exam_Data"
gdb_name = "GPS_Results.gdb"
arcpy.CreateFileGDB_management(gdb_path, gdb_name)

#Create feature dataset inside newly created geodatabase
out_name = "Study_Areas"
out_dataset = arcpy.CreateFeatureDataset_management(gdb_name, out_name)

#Set spatial reference and projection
sr = arcpy.SpatialReference("NAD 1983 UTM Zone 12N")
arcpy.DefineProjection_management(out_dataset, sr)
 
#Create a shapefile of each sheet with X, Y data from an excel file
excelfile = xlrd.open_workbook("C:/GIS_Programming/Final_Exam_Data/GPS.xlsx")
for sheet in excelfile.sheets():
    newfc = sheet.name
    out_data = "C:/GIS_Programming/Final_Exam_Data/GPS_Results.gdb/Study_Areas/"
    shapefiles = arcpy.CreateFeatureclass_management(out_data, newfc, "Point", spatial_reference = sr)
    cursor = arcpy.da.InsertCursor(shapefiles, ["SHAPE@"])
    point = arcpy.Point()
    for row in range (1, sheet.nrows):
        point.ID, point.X, point.Y = sheet.row_values(row)
        cursor.insertRow([point])
    del cursor
