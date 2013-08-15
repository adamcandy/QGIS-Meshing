# Take the coords of the domain as well as that of the boundary polygons, a default ID and list of ID's contained inside the boundary-polygons. For the exterior of the domain it will create Shapely Lines from sequential points and see if the line intersects one of the boundary-polygons. For the islands: creates a Shapely polygon for each island and sees if it is fully enclosed within any of the boundary-ID polygons. 

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

#Returns a tuple of 2 elements: element 1 contains a list of lines that compose the external line loop of the domain; element 2 is the ID associated with each line along with a list of tuples, element 1 of the tuple is the island and element 2 is the ID of that island.
# ([line1, line2, linex], [1, 2, x]), [(polygon1, ID1), (polygon2, ID2)...]

# Second function, connectLines joins sequential lines if they share the same ID number.

import shapefile
from shapely.geometry import *


class assignIDs():
	def assignIDsMethod(self, idShapeFile):
		print 'assignID'

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
		print 'assignID', self.domainData.points
		

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
