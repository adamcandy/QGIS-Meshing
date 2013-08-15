"""

##########################################################################
#  
#  QGIS-meshing plugins.
#  
#  Copyright (C) 2012-2013 Imperial College London and others.
#  
#  Please see the AUTHORS file in the main source directory for a
#  full list of copyright holders.
#  
#  Dr Adam S. Candy, adam.candy@imperial.ac.uk
#  Applied Modelling and Computation Group
#  Department of Earth Science and Engineering
#  Imperial College London
#  
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation,
#  version 2.1 of the License.
#  
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#  
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307
#  USA
#  
##########################################################################

Sets the read and the write file stream according to
the command line arguments given.

The first argument specifies which shape file the user
wants to specify the boundaries of

The second arguments specifies the boundary polygon

The third argument specifies the file path to which the
new shape has to be written
"""


from shapely.ops import cascaded_union
import shapefile
from shapely.geometry import *
import sys
import matplotlib.pyplot as pyplot

"""
Write the results to .shp.
"""
def writeShapeFile(points, filepath) :
	#begin the instance pf writer class
	w = shapefile.Writer()
	#ensure shape and records the balance
	w.autobalance = 1
	i = 0
	for l in points:
		pList = []
		pList.append(l)
		if len(l)==1 :
			w.point(pList[0][0],pList[0][1])
			w.field("%d_FLD"%i,"C","40")	
			i+=1
		elif len(l)==2 :
			w.line(parts = pList)
			w.field("%d_FLD"%i,"C","40")		
			i+=1
		else :
			w.poly(parts = pList)
			w.field("%d_FLD"%i,"C","40")
			i += 1
	w.save(filepath)
	print("Number of shapes Written %d" %i)


"""
Used if there is only one shape in the boundary shapefile.
"""
def getBoundaryPointsList(bounds):
	shapes = bounds.shapes()
	pointsList = (shapes[0].points)
	polygon = Polygon(pointsList)
	return (polygon,pointsList)

"""
When more than one shapefile, works out which objects from the .shp file are overlapping and return the exterior coords of this new shape.
"""
def overlap (bounds, plot = False):
# Read shapefile and work out overlap. Optional plot.
	shapes = bounds.shapes()
	pointsList = []
	for i in range(len(shapes)):
		# Check datapoint is valid.
		pointsList.append(shapes[i].points)

	# Turn the points into polygons.
	polygons = []
	for j in range(len(pointsList)):
		polygons.append(Polygon([pointsList[j][i] for i in range(len(pointsList[j]))]))

	# Add overlapping shapes into a list so we know which to join together.
	overlapping = []
	for n in range(len(polygons) - 1):
		if polygons[n].intersects(polygons[n+1]) == True: 
			# Two if statements to make sure the same polygon isn't being entered more than once.
			if polygons[n] not in overlapping: overlapping.append(polygons[n]) 
			if polygons[n + 1] not in overlapping: overlapping.append(polygons[n + 1]) 

	# Create a new shape from the overlapping shapes.
	join = cascaded_union(overlapping)
	poly = [join]

	# Take the coords. of the perimeter of this new shape.
	coords = []
	for i in range(len(join.exterior.coords)):
		coords.append(list(join.exterior.coords[i]))


	# Plot results if True. Store x-y coords of the perimeter in two lists to plot.
	if plot == True:
		x = []; y = []
		for i in range(len(coords)):
			x.append(coords[i][0]); y.append(coords[i][1])

		# Plot results.
		pyplot.plot(x, y)
		pyplot.xlim(-4, 4)
		pyplot.ylim(-4, 4)
		pyplot.show()
	return join, coords



"""
Output the final results as a .geo file.
"""
def write_geo (coords, filename):
# Write new shape to .geo.
	print coords

	target = open("%s.geo" % filename, "w") # Creates .geo file to write to.
	for i in range(len(coords)):
		# Write point.
		target.write('Point(%d) = {%.3f, %.3f, 0, %.3f};\n' %(i + 1, coords[i][0], coords[i][1], 1.0))
		# Write the lines connecting the sequential points.
		if (i + 1 > 1): target.write('Line(%d) = {%d, %d};\n' % (i, i, i + 1))
	# Connect first and last points.
	target.write('Line(%d) = {%d, %d};\n' % (i + 1, 1, i + 1))
	target.close()
	return False


assert len(sys.argv)==5, "Incorrect Number of Arguments passed"

readPath = sys.argv[1]
boundaryPath = sys.argv[2]
writePath = sys.argv[3]
areaThreshold = float(sys.argv[4])

#input stream for the given shape
sf = shapefile.Reader(readPath)

#shapes contained in the given file
shapes = sf.shapes();

#boundary = bounds.shapes[0]
boundary = shapefile.Reader(boundaryPath)

if (len(boundary.shapes()) > 1): boundaryPolygons, boundaryPointList1 = overlap(boundary); boundaryPointList = [boundaryPointList1]
else: boundaryPolygons, boundaryPointList = getBoundaryPointsList(boundary)

"""
Takes shape from shapefile and converts to a Shapely Polygon. Checks if this polygon lies within the boundary using a.intersect(b). If it does it will perform a.intersection(b) operation returning a Polygon/MultiPolygon which lies within the boundary and then plots result.
"""
shapeList = []
for shape in shapes:
	x = []; y = []; shp = []
	polygon = Polygon([shape.points[i] for i in range(len(shape.points))])
	if (polygon.intersects(boundaryPolygons)):
		intersection = boundaryPolygons.intersection(polygon)
		if intersection.area >= areaThreshold:

			if intersection.geom_type == 'Polygon':
				for i in range(len(list(intersection.exterior.coords))):
					x.append(intersection.exterior.coords[i][0]); y.append(intersection.exterior.coords[i][1])
					pyplot.plot(x, y)
					shp.append([intersection.exterior.coords[i][0], intersection.exterior.coords[i][1]])

			if intersection.geom_type == 'MultiPolygon':
				for j in range(len(intersection)):
					for i in range(len(list(intersection[j].exterior.coords))):
						x.append(intersection[j].exterior.coords[i][0]); y.append(intersection[j].exterior.coords[i][1])
						pyplot.plot(x, y)
						shp.append([intersection[j].exterior.coords[i][0], intersection[j].exterior.coords[i][1]])
			shapeList.append(shp)
writeShapeFile(shapeList, writePath)

# Plot boundary.
x=[]
y=[]

for i in range(len(boundaryPointList)):
	x.append(boundaryPointList[i][0]); y.append(boundaryPointList[i][1])
pyplot.plot(x,y)
pyplot.xlim(min(x)-1,max(x)+1)
pyplot.ylim(min(y)-1,max(y)+1)

pyplot.show()
