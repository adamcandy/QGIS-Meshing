# Take the coords of the domain as well as that of the boundary polygons, a default ID and list of ID's contained inside the boundary-polygons. For the exterior of the domain it will create Shapely Lines from sequential points and see if the line intersects one of the boundary-polygons. For the islands: creates a Shapely polygon for each island and sees if it is fully enclosed within any of the boundary-ID polygons. 

#Returns a tuple of 2 elements: element 1 contains a list of lines that compose the external line loop of the domain; element 2 is the ID associated with each line along with a list of tuples, element 1 of the tuple is the island and element 2 is the ID of that island.
# ([line1, line2, linex], [1, 2, x]), [(polygon1, ID1), (polygon2, ID2)...]

# Second function, connectLines joins sequential lines if they share the same ID number.

import shapefile
from shapely.geometry import *

#must redefine to accept multiple domains

class assignIDs(): #for some reason seems to be yeilding an earlier result
	def __init__(self,domainCoordsList, IDPolygonCoordsList, defaultID, domainID, IDPolygonID, threshold, idShapeFile):
		self.domainCoordsList = domainCoordsList
		self.IDPolygonCoordsList = IDPolygonCoordsList
		self.defaultID = defaultID
		self.IDPolygonID = IDPolygonID
		self.threshold = threshold
		self.domainID = domainID		
		# Generate a list of Shapely polygons from the coordinates of the boundary-ID polygons.
		self.boundaryIDList = []		
		self.idShapeFile = idShapeFile
		self.IDPolygons = []
		for j in range(len(self.IDPolygonCoordsList)):
			self.IDPolygons.append(Polygon([self.IDPolygonCoordsList[j][i] for i in range(len(self.IDPolygonCoordsList[j]))]))
		self.physicalIslandList = []
		self.lineIDList = []

		# i = 0 is the exterior boundary line. Break this into component lines and see which of these intersect the boundary polygons.
		for i in range(len(self.domainCoordsList)):
				self.generateIds(i)
		
		self.result = self.boundaryIDList, domainCoordsList
		#self.result = (self.physicalBoundaryLineList, self.boundaryIDList), self.physicalIslandList, (self.islandBoundaryList, self.islandLineIDList)

	def generateIds(self, part):
		localIdList = []
		for j in range(len(self.domainCoordsList[part]) - 1):
			# Want to make a shapely line from sequential points.
			line = LineString([tuple(self.domainCoordsList[part][j]), tuple(self.domainCoordsList[part][j + 1])])
			

	#		if not self.idShapeFile:
	#			for n in range(len(self.IDPolygons)):
	#				localIdList.append(self.defaultID)
	#			return
			done = False
			for n in range(len(self.IDPolygons)):

				if line.intersects(self.IDPolygons[-(n+1)]):
					#print "Now", self.IDPolygonID[-(n+1)][0]
					if self.idShapeFile:
						localIdList.append(self.IDPolygonID[-(n+1)][0])
					else:
						localIdList.append(self.defaultID)
					done = True
					break

			if not done:
				localIdList.append(self.defaultID)

		
		self.boundaryIDList.append(localIdList)



def connectLines (bounds):
	
	lineLists = []
	for points in bounds:
		localLines = []
		for i in range(len(points)-1):
			point1 = points[i]
			point2 = points[i+1]
			localLines.append((point1, point2))
		lineLists.append(localLines)
	"""
	for i in range(len(bounds[1]) - 1):
		if bounds[1][i] != bounds[1][i + 1]:
			elementList.append(i + 1)

	elementList.append(len(bounds[1]))
	
	connectedLinesList = []
	IDList = []
	for i in range(len(elementList) - 1):
		connectedLine = MultiLineString(bounds[0][elementList[i] : elementList[i + 1]])
		connectedLinesList.append(connectedLine)
		IDList.append(boundaryCoordsandIDList[1][elementList[i]])"""

	#return (connectedLinesList, IDList)
	return lineLists
