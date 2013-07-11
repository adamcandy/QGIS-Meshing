#Function to write .shp files. Read these files in new function, use shapely to work out overlap. Output this new shape to .geo using another function.

from shapely.geometry import Polygon
from shapely.geometry.polygon import LinearRing
import shapefile

"""
The local variable __error_occured keeps a track during the program
if any error occurs. The value of __error_occured is set to 1 if
program does not execute properly
"""
__error_occured = 0

"""
The variable threshold  defines the threshold value for the area of
islands which has to be ignored while writing the .geo file.
Any island which has a area less than the threshold are not written
to the .geo file
"""
__threshold = 0.01

"""
This method gets the points of the all the shapes in the shapefile given
@param filename : specifies the filepath of the shapefile which has
									to be converted to .geo file
@return					: returns a list of points containing all the points
									for the shapes within the shapefile. The shapes which
									has area less than threshold value are ignored. Also
									returns an empty list on error
"""
def __getPointsList(filename):
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
				if len(pList)>2 and Polygon(pList).area>__threshold:# and Polygon(pList).is_ring:
					pointsList.append(pList)
	except IOError:
		__error_occured = 1
		return []
	return pointsList

"""
This method performs an and operation on the given array
@param array : specifies the array on which the and operation has
							 to be performed
@return			 : returns true iff all values in the given array are 
							 true and false otherwise
"""
def __and_of_array(array):
	for elem in array:
		if elem==False:
			return False
	return True

"""
This method returns the index for the outer most polygon, i.e. the exterior
of the given shapefile.
@param coords : contains the co-ordinates of all the shapes in from the
                given shapefile
@return       : returns the index of the shape which is the exterior
"""
def __get_exterior_index(coords):
	exterior_index = -1
	for i in range(len(coords)):
		pts = coords[i]
	 	poly = Polygon(pts)
	 	res = []
	 	for p in coords:
	 		res.append(poly.contains(Polygon(p)))
		if __and_of_array(res) : return i+1
	__error_occured=1
	return -1

"""
This methods uses the given co-ordinates and writes them to a .geo file
at the filepath specified.
@param coords   : specifies the co-ordinates of the shapes which has to
									be written to the shapefile
@param filename : specifies the filepath where .geo file has to be saved

"""
def __write_geo (coords, filename):
	try : 
		target = open("%s.geo" % filename, "w") # Creates .geo file to write to.
	except IOError:
		__error_occured = 1
		return 
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
		target.write(surface)
	except IOError:
		__error_occured = 1
		return []
	finally:
		target.close()

"""
This method is the main emthod for this script and uses auxilary methods
in the module to generate the .geo file from the shapefile
@param readPath  : specifies the filepath of the shapefile which has
									 to be converted
@param writePath : specifies the filepath to write the .geo file
@param t				 : specifies the threshold value for the area. The
									 default value for threshold is set to 0.01
"""
def getGeoFile(readPath,writePath,t=0.01):
 	pointsList = __getPointsList(readPath)
 	if __error_occured == 1 :
 		return 1
	__write_geo(pointsList, writePath)
	return __error_occured
