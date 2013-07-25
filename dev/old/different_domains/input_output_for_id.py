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

This is a helper module for the plugin which deals with assigning id's 
to allow it to be used in fluidity
"""

import shapefile
from shapely.geometry import MultiLineString, Polygon
import sys

__islandField = "Island"
__boundaryField = "Boundary"

"""
This method gets the points of the all the shapes in the shapefile given
@param filename : 	specifies the filepath of the shapefile which has
					to be converted to .geo file
@return	: 	returns a list of points containing all the points
			for the shapes within the shapefile and the records
			of the given shapefile
"""

class ShapeData:

	def __init__(self, filename, threshold, is_domain):
		try:
			bounds = shapefile.Reader(str(filename))
		except shapefile.ShapefileException:
			sys.exit()
		try:
			records = bounds.records()
			regionIDs = []
			pointsList = []
			shapes = bounds.shapes()
			shapeList = []
			PartNumber = 0
			for shapeNo in range(len(shapes)):
				shape = shapes[shapeNo]
				ID = records[shapeNo][0]
				points = shape.points
				splitPoints = shape.parts
				shapeList.append(PartNumber)
				if len(splitPoints) == 1 :
					pointsList.append(points)
					regionIDs.append(ID)
					PartNumber += 1
				else:
					splitPoints.append(len(points)-1)
					for i in range(len(splitPoints)-1):
						ptList = (points[splitPoints[i]:splitPoints[i+1]])
						if is_domain and Polygon(ptList).area > threshold:
							regionIDs.append(ID)
				 			pointsList.append(ptList)
							PartNumber += 1
		except IOError:
				sys.exit()

		self.points = pointsList
		self.records = records
		self.regionIDs = regionIDs
		self.shapes = shapeList


	"""
	This method write the given shapes into a shapefile making sure
	that all the islands are saved with field island and all boundaries
	are saved with field boundary.
	@param boundary : is a tuple consisting of the lines in boundary with
																		its id
	@param islands  : specifies the polygon for the island and the id for it

	"""
	def __saveShapeFile(self, boundaryIds, bounds, filepath):
		w = shapefile.Writer()
		#bounds, boundaryID = boundary
		filepath = str(filepath)
		w.field("id","c","40")
		w.field("type","c","40")		
		w.shapetype = shapefile.POLYLINE
		print len(bounds)
		print len(boundaryIds)
		for i in range(len(bounds)):

			for j in range(len(bounds[i])):
				line = bounds[i][j]
				lineID = boundaryIds[i][j]
				w.line(parts = [[line[0],line[1]]])
				w.record(str(lineID),str(i))
		
		w.save(filepath)				

