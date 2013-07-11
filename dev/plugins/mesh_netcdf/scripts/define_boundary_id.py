# Take the coords of the domain as well as that of the boundary polygons, a default ID and list of ID's contained inside the boundary-polygons. For the exterior of the domain it will create Shapely Lines from sequential points and see if the line intersects one of the boundary-polygons. For the islands: creates a Shapely polygon for each island and sees if it is fully enclosed within any of the boundary-ID polygons. 

#Returns a tuple of 2 elements: element 1 contains a list of lines that compose the external line loop of the domain; element 2 is the ID associated with each line along with a list of tuples, element 1 of the tuple is the island and element 2 is the ID of that island.
# ([line1, line2, linex], [1, 2, x]), [(polygon1, ID1), (polygon2, ID2)...]

# Second function, connectLines joins sequential lines if they share the same ID number.

import shapefile
from shapely.geometry import *


class assignIDs():
	def assignIDsMethod(self, idShapeFile):

		# Generate a list of Shapely polygons from the coordinates of the boundary-ID polygons.
		self.boundaryIDList = []		
		self.idShapeFile = idShapeFile
		self.IDPolygons = []
		if idShapeFile:
			for j in range(len(self.boundaryData.points)):
				self.IDPolygons.append(Polygon([self.boundaryData.points[j][i] for i in range(len(self.boundaryData.points[j]))]))

		# Break into component lines and see which intersect the boundary polygons.
		for i in range(len(self.domainData.points)):
				self.generateIds(i)
		

	def generateIds(self, part):
		localIdList = []
		for j in range(len(self.domainData.points[part]) - 1):
			if not self.idShapeFile:
				localIdList.append(self.defID)
				continue
			self.methodIDPolygons(localIdList, part, j)
		self.boundaryIDList.append(localIdList)


	def methodIDPolygons(self, localIdList, part, j):

		# Want to make a shapely line from sequential points.
		line = LineString([tuple(self.domainData.points[part][j]), tuple(self.domainData.points[part][j + 1])])
		done = False
		for n in range(len(self.IDPolygons)):
			if line.intersects(self.IDPolygons[-(n+1)]):
				localIdList.append(self.boundaryData.records[-(n+1)][0])
				done = True
				break
		if not done:
			localIdList.append(self.defID)



def connectLines (bounds):
	
	lineLists = []
	for points in bounds:
		localLines = []
		for i in range(len(points)-1):
			point1 = points[i]
			point2 = points[i+1]
			localLines.append((point1, point2))
		lineLists.append(localLines)

	return lineLists
