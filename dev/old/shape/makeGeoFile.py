#Function to write .shp files. Read these files in new function, use shapely to work out overlap. Output this new shape to .geo using another function.

from shapely.geometry import Polygon
from shapely.geometry.polygon import LinearRing
import shapefile
import sys

#defualt value for threshold is 0
threshold = 0.01

class Errors:
  SHAPEFILE_ERROR = "ERROR: Unable to open the file. Please check the path of the file"
  INVALID_SHAPEFILE_ERROR = "ERROR : Invalid Shapefile. Please use a shapefile output from QGIS"
  OPEN_GEO_ERROR = "ERROR : Invalid path to write the .geo File"
  WRITING_GEO_ERROR = "ERROR: Error in writing to the file. Please check if any other external programs are using the same file."
  INVALID_THRESHOLD_ERROR = "Invalid Threshold Value: Please enter an integer for the value of threshold (0 if no threshold is required)"

def getPointsList(filename):
	try:
		bounds = shapefile.Reader(filename)
	except shapefile.ShapefileException:
		print(Errors.SHAPEFILE_ERROR)
		sys.exit()
	try:
		shapes = bounds.shapes() 
		for shape in shapes :
			points = shape.points
			splitPoints = shape.parts
			pointsList = []		
			for i in range(len(splitPoints)-1):
				pList = points[splitPoints[i]:splitPoints[i+1]]
				#print (Polygon(pList).area)
				if len(pList)>2 and Polygon(pList).area>threshold:# and Polygon(pList).is_ring:
					pointsList.append(pList)
	except IOError:
		print(Errors.INVALID_SHAPEFILE_ERROR)
		sys.exit()
	return pointsList


# Write new shape to .geo.
def write_geo (coords, filename):
	try : 
		target = open("%s.geo" % filename, "w") # Creates .geo file to write to.
	except IOError:
		print(Errors.OPEN_GEO_ERROR)
		sys.exit()
	i = 0
	try :
		for l in coords:
			# Write point.
			for p in l:
				print(p)
				i +=1
				target.write('Point(%d) = {%f, %f, 0, 1.0};\n' %(i, p[0], p[1]))
		# Write the lines connecting the sequential points.
		i=0
		c = 0
		surface = "Plane Surface(1) = {"
		for k in range(len(coords)):
			l = coords[k]
			i+=1
			lineloop = "Line Loop(%d) = {" % i		
			for j in range(len(l)-1) :
				target.write("Line(%d) = {%d,%d};\n"%((j+c+1),(c+j+1),(j+c+2)))
				lineloop = lineloop + str(j+c+1) + ", "
			target.write("Line(%d) = {%d,%d};\n"%((c+len(l)),(c+ len(l)),(c+1)))
			lineloop = lineloop + ("%d};\n"%(len(l)+c))
			target.write(lineloop)
			surface = surface + str(i) + ", "
			c+=len(l)
		if len(surface)!= 20 : surface = surface[0:len(surface)-2]
		surface = surface + "};\n"
	except IOError:
		print(Errors.WRITING_GEO_ERROR)
		sys.exit()
	finally:
		target.write(surface)
		target.close()
			
def printUsage():
	print("ERROR INCORRECT USAGE\nProgram Usage:\n$ python <NAME OF THE SCRIPT TO WRITE GEO> <PATH OF SHAPEFILE> <PATH TO SAVE GEO> <THRESHOLD VALUE (DEFUALT=0.01)")


if len(sys.argv)!=4 and len(sys.argv)!=3:
	printUsage()
	sys.exit()
readPath = sys.argv[1]
writePath = sys.argv[2]
if len(sys.argv)==4 :
  try:
	  threshold = float(sys.argv[3])
  except ValueError:
	  print(Errors.INVALID_THRESHOLD_ERROR)
	  sys.exit()
print("writing the file")
write_geo(getPointsList(readPath), writePath)
print("File has been written")
