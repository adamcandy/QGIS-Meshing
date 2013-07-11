
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
	
