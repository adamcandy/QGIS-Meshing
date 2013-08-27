import shapefile

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

from shapely.geometry import *
import sys
import matplotlib.pyplot as pyplot

def checkIfPointIsInPointList(points, pt):
	for p in points:
		if p[0]==pt.x and p[1]== pt.y:
			return True
	return False

"""
	This function checks if the given point is on the boundary.
	@param point : specifies the point which has to be checked
	@param bouds : specifies all the bpundary objects
	@return			 : retucheckPointOnBoundary(p, boundaryPointList)rns true iff the point in on the boundary lines
	print coords
"""
def checkPointOnBoundary(point, boundaryPoints):
	for points in boundaryPoints:
		if checkIfPointIsInPointList(points, p):
			return True
	#for s in bounds.shapes():
		numberOfPoints = len(points)
		for i in range(numberOfPoints-1):
			line = LineString([(points[i][0],points[i][1]),(points[i+1][0], points[i+1][1])])
			if (line.contains(point)):
				return True
	return False

"""
This method returns a list of all the boundary points 
on the boundaries given. This method also returns polygons
consited of the given shapes
@param bounds : specfies the boundary shapes
@return				: returns a tuple containing the polygons shapes
								of the boundary and the exterior points list for
								them
"""
def getBoundaryPointsList(bounds):
	shapes = bounds.shapes()
	pointsList = []
	for i in range(len(shapes)):
		pointsList.append(shapes[i].points)
	polygons = []
	for j in range(len(pointsList)):
		polygons.append(Polygon([pointsList[j][i] for i in range(len(pointsList[j]))]))
	return (polygons,pointsList)


def check_point_within_boundary(p, boundaries):
	for poly in boundaries :
		if p.within(poly):
			return True
	return False

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


#check if the number of command  line arguments are 
#ok
assert len(sys.argv)==4, "Incorrect Nu	mber of Arguments passed"

"""
Sets the read and the write file stream according to
the command line arguments given.

The first argument specifies which shape file the user
wants to specify the boundaries of

The second arguments specifies the boundary polygon

The third argument specifies the file path to which the
new shape has top be written

"""

readPath = sys.argv[1]	
boundaryPath = sys.argv[2]
writePath = sys.argv[3]

#input stream for the given shape
sf = shapefile.Reader(readPath)

#input stream of the boundaries
#bounds = shapefile.Reader(boundaryPath)

#shapes contained in the given file
shapes = sf.shapes();
	
#checks that there shouldonly be one boudary
#assert len(bounds.shapes())==1, "More than one shape in the boundary. Currently only one shape can be specified as a boundary"

#boundary = bounds.shapes[0]
boundary = shapefile.Reader(boundaryPath)

# Create list of the points defined in the .shp file.
pointslist = []
for i in range(len(shapes)):
	# Check datapoint is valid.
	pointslist.append(shapes[i].points)


boundaryPolygons, boundaryPointList = getBoundaryPointsList(boundary)

	
i = -1
c = 1
points  = []
list_to_save = []
for shape in shapes:
	i += 1
	x =[]; y=[]
	pList = []
	for point in pointslist[i]:
		p = Point(point[0],point[1])
		if check_point_within_boundary(p, boundaryPolygons) or checkPointOnBoundary(p, boundaryPointList) :
			x.append(p.x)
			y.append(p.y)
			points.append(p)
			pList.append(point)
		c +=1
		pyplot.plot(x,y)
	if len(pList)>0 :
		list_to_save.append(pList)

for p in points:
	print(p)

if (len(list_to_save)>0) : writeShapeFile(list_to_save,writePath)

x=[]
y=[]
for p in boundaryPointList :
	for p2 in p :
		x.append(p2[0])
		y.append(p2[1])
pyplot.plot(x,y)
pyplot.xlim(min(x)-1,max(x)+1)
pyplot.ylim(min(y)-1,max(y)+1)
pyplot.show()
