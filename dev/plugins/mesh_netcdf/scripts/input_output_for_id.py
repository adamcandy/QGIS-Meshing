"""
This is a helper module for the plugin which deals with assigning id's 
to allow it to be used in fluidity
"""

import shapefile
from shapely.geometry import MultiLineString, Polygon
import sys
from numpy import pi, cos, sin, array

__islandField = "Island"
__boundaryField = "Boundary"

R = 6.3781e6

"""
This method gets the points of the all the shapes in the shapefile given
@param filename : 	specifies the filename of the shapefile which has
					to be converted to .geo file
@return	: 	returns a list of points containing all the points
			for the shapes within the shapefile and the records
			of the given shapefile
"""

class ShapeData:

  def __init__(self, filename, threshold, is_domain):
    #try:
    bounds = shapefile.Reader(str(filename))
    #except shapefile.ShapefileException:
    #raise AssertionError()
    try:
      records = bounds.records()
      regionIDs = []
      pointsList = []
      shapes = bounds.shapes()
      shapeList = []
      PartNumber = 0
      # Loop through shape-records and extract point coordinates and
      #  Regiod IDs
      for shapeNo in range(len(shapes)):
        shape = shapes[shapeNo]
        ID = records[shapeNo][0]
        points = shape.points
        shapeParts = shape.parts
        print shapeParts
        shapeList.append(PartNumber)
        if len(shapeParts) == 1 :
          pointsList.append(points)
          regionIDs.append(ID)
          PartNumber += 1
        else:
          shapeParts.append(len(points)-1)
          for i in range(len(shapeParts)-1):
            ptList = (points[shapeParts[i]:shapeParts[i+1]])
            phi = array(Polygon(ptList).bounds)*pi/180
            Sf = 2*34*pi*R**2*(phi[3]*sin(phi[3])-phi[1]*sin(phi[1]))/(pi*(phi[3]-phi[1])*1000000000000)
            area = abs(Polygon(ptList).area*Sf)
            if is_domain and area > threshold:
              regionIDs.append(ID)
              pointsList.append(ptList)
              PartNumber += 1
            if is_domain :
              pointsList[-1].append(pointsList[-1][0])

    except IOError:
      raise AssertionError()

    self.points = pointsList
    self.records = records
    self.regionIDs = regionIDs
    self.shapes = shapeList


  def __saveShapeFile(self, boundaryIds, bounds, filename):
    """
    This method writes the given shapes into a shapefile, as
    Polylines. The polylines are assigned user-specified IDs
    (boundaryIds) as shapefile records.
    """
    w = shapefile.Writer()
    filename = str(filename)
    w.field("id","c","40")
    w.field("type","c","40")		
    w.shapetype = shapefile.POLYLINE
    for i in range(len(bounds)):
       for j in range(len(bounds[i])):
         line = bounds[i][j]
         lineID = boundaryIds[i][j]
         w.line(parts = [[line[0],line[1]]])
         w.record(str(lineID),str(i))

    w.save(filename)				

  def get_shapes(self):
    """
    Method for returning the shapes in a shapefile.
    """
    return self.shapes

