
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
This is a helper module for the plugin which deals with assigning id's 
to allow it to be used in fluidity
"""

import shapefile
from shapely.geometry import MultiLineString, Polygon
import sys
from numpy import pi, cos, sin, array, arange

__islandField = "Island"
__boundaryField = "Boundary"

R = 6.3781e6

"""
This method gets the points of the all the shapes in the shapefile given
@param filename :   specifies the filename of the shapefile which has
          to be converted to .geo file
@return  :   returns a list of points containing all the points
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
      pointsList = []#this can be left as is its the lines which need a consistent mapping
      RegionId = []#note this maps to lines
      LLoopMap = []
      ShapeMap = []
      shapes = bounds.shapes()
      shapeList = []
      PartNumber = 0
      # Loop through shape-records and extract point coordinates and
      #  Regiod IDs
      for shapeNo in range(len(shapes)):
        shape = shapes[shapeNo]
        ID = records[shapeNo][0]
        points = shape.points
        shapeParts = shape.parts #could do loopcorrect on this instead
        #loopcorrect = range(len(shapeParts))
        #for i in loopcorrect:
        #  shapeParts[i] -= i
        shapeList.append(PartNumber)
        if len(shapeParts) == 1 :
          pointsList.append(points)
          regionIDs.append(ID)
          PartNumber += 1
          shapeParts.append(len(points)-1)#hopefully this won't break it
        else:
          shapeParts.append(len(points)-1)#this is whats causing the difficulty - yes
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
        LLoopMap += shapeParts #this works as no of points = no of lines - assuming points not doubled up, may need -1
        ShapeMap += [shapeParts[-1]]#this should be again be fine given proviso of above
        RegionId += [ID]#this should be fine
      
    except IOError:
      raise AssertionError()


    #will change the output of this
    self.points = pointsList
    self.pointsList = [point for part in pointsList for point in part]

    #conflicts = 0
    #for i in range(len(self.pointsList) - 1):
    #  i -= conflicts
    #  if self.pointsList[i] == self.pointsList[i+1]:
    #    del self.pointsList[i+1]
    #    conflicts += 1


    self.records = records
    self.regionIDs = regionIDs
    self.shapes = shapeList
    self.RegionId = RegionId
    self.LLoopMap = LLoopMap
    self.ShapeMap = ShapeMap

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

