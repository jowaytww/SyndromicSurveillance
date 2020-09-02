import ogr,csv,sys
import os 
command = "ogr2ogr -f CSV {} {} -lco GEOMETRY=AS_WKT".format(r"C:\Users\GANDHIS\Desktop\Python scripts\output-WKT.csv",r"C:\Users\GANDHIS\Desktop\Python scripts\tl_2019_39_unsd_SchoolDistrict_OH_2019\tl_2019_39_unsd.shp")
os.system(command)
