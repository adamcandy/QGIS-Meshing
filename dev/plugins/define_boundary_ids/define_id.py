from input_output_for_id import getShapeData,saveShapeFile
from define_boundary_id import *

def define_bounds(boundaryPath, domainPath, writePath, defID, threshold):

        print "Getting the shape data"
        domainPoints, domainRecords, boundaryPoints,boundaryRecords = getShapeData(domainPath, boundaryPath)
        print "Attempting to assign ids" 
	boundaryIds, bounds = assignIDs(domainPoints, boundaryPoints, defID, domainRecords, boundaryRecords, threshold, boundaryPath != domainPath).result
	bounds = connectLines(bounds)
        print "Saving the shapefile"  
	saveShapeFile(boundaryIds, bounds, writePath)
	
		
