

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

"""
	This function checks if the given point is on the boundary.
	@param point : specifies the point which has to be checked
	@param bouds : specifies all the bpundary objects
	@return			 : returns true iff the point in on the boundary lines
"""
def checkPointOnBoundary(point, bounds, boundaryPoints):
	i = 0
	for boundary in bounds :
		if (point.x,point.y) in boundaryPoints[i]:
			return True
	#for s in bounds.shapes():
		points = boundaryPoints[i]
		numberOfPoints = len(points)
		for i in range(numberOfPoints-1):
			line = LineString([(points[i][0],points[i][1]),(points[i+1][0], points[i+1][1])])
			if (line.contains(point)):
				return True
		i += 1
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
	
