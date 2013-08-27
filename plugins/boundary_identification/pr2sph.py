import sys

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

import shapefile
import math

 
#This script projects a shapefile to a sphere. It projects each points to the sphere and then connects the lines using curved lines (so that they won't intersect the sphere.

#In case the user enters a wrong input:
def usage():
	print "Usage:\n$ python <NAME OF SCRIPT> <PATH OF .shp> <PATH TO WRITE>"

#Self-explainitory:
def same_point(x1,y1,x2,y2):
  dist = math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
  return (dist<=0.000001)

#The two arguments: a shapefile and a path to the .geo file.
def export(shp, geo):
   shpFile = shp 
   lookupTable = []
   geoFile =  open(geo,"w")
   
   # Extracting the shapes and the records.
   
   shapes =  shpFile.shapes()
   records = shpFile.records()
   
   # Creating a sphere with the radius of the earth: 
   print "Writing .geo file!"
   geoFile.write("//Projection of a plane on a sphere:\n\n\n")
   geoFile.write("Point(1) = {0.0,0.0,0.0}; //The center of the sphere\n")
   geoFile.write("Point(2) = {0.0,0.0,6.37101e+06}; //The North Pole\n")
   geoFile.write("PolarSphere(1) = {1,2};\n")

   # Point ids have to start from 3 (1 and 2 are already used). For convenience, I'll make the lines start at 3 as well.

   pId = 3
   lId = 3
   
   # We're using 2d, so there is no z (z is zero). meshSize is not used but assigned just in case, so that it will be ready for usage.

   zCoord = 0
   meshSize = 2
   lLoop = 1
   phLine = []
   lookupTable.append(0)
   lookupTable.append(0)
   lookupTable.append(0)
   geoFile.write("zCoord = %f;\n" %zCoord)
   geoFile.write("meshSize = %f;\n" %meshSize)

   # Each point need to be projected to the sphere first.

   for i in range(len(shapes)):
     for j in range(len(shapes[i].points)):
       longitude = shapes[i].points[j][0]
       latitude  = shapes[i].points[j][1]
       cos = math.cos
       sin = math.sin
       longitude_rad = math.radians(- longitude - 90)
       latitude_rad  = math.radians(latitude)
       x = sin( longitude_rad ) * cos( latitude_rad ) / ( 1 + sin( latitude_rad ) )
       y = cos( longitude_rad ) * cos( latitude_rad  ) / ( 1 + sin( latitude_rad ) )
       shapes[i].points[j][0] = x
       shapes[i].points[j][1] = y

   # The duplicate points are removed. It's important for this to be done after the actual projection, otherwise there will be overlaping points in GMsh.

   for i in range(len(shapes)):
     for j in range(len(shapes[i].points)-1):
       while j < len(shapes[i].points)-1 and same_point(shapes[i].points[j][0], shapes[i].points[j][1], shapes[i].points[j+1][0], shapes[i].points[j+1][1]):
         trash = shapes[i].points.pop(j+1)
     trash = shapes[i].points.pop()
   i = 0
 
   # The deleting of many unnecesary points can cause empty shapes to appear, which would cause bugs later on. Here we check for any empty shapes and remove them as well as their specific records:

   while i < len(shapes):
     if(len(shapes[i].points) == 0):
       trash = shapes.pop(i)
       trash = records.pop(i)
     else:
       i+=1 


   # This for-loop extracts all the points, one by one, and writes them as it goes along

   for i in range(len(shapes)):
     shape = shapes[i]
     for coord in shape.points:
       geoFile.write("Point(%d) = {%f, %f, zCoord};\n" %(pId, coord[0], coord[1]))
       pId+=1

   # Resent the point and line ids so that we can begin to write the lines:

   pId = 3
   lId = 3
   i = 0
   lLoopId = 1
   planeSurface = "Plane Surface(1)={"

   # This loop writes the lineloops and the curved lines. polyId makes sure that each polygon is written in exactly one loop. The id is added to phLine (physical lines). The lookupTable will retain which line lies in what lineloop.

   while i < len(shapes):
     init = pId
     polyId = records[i][1]
     lLoop = "Line Loop(" + str(lLoopId) + ") = {"
     while(i<len(shapes) and polyId == records[i][1]):
       shape = shapes[i]
       for j in range(len(shape.points)):
         if j==len(shape.points)-1 and (i+1>=len(shapes) or polyId!=records[i+1][1]):
           geoFile.write("BSpline(%d) = {%d, %d};\n" %(lId ,pId, init))
         else:
           geoFile.write("BSpline(%d) = {%d, %d};\n" %(lId, pId, pId+1))
         phLine.append((int(records[i][0]),lId))
         lookupTable.append(lLoopId)
         lId+=1
         pId+=1
       i+=1
     lLoop+=str(init) + " : " + str(pId-1) + "};\n"
     geoFile.write(lLoop)
     if lLoopId>1:
       planeSurface += ", " + str(lLoopId)
     else:
       planeSurface += str(lLoopId)
     lLoopId+=1
   geoFile.write("\n")

   # We have written the actual geometric figure by this point. Now we need to assign the ids. I'll be using compound lines to minimize the number of points used:

   pId = 3
   i = 0
   lLoopId = 1
   idList = []
   while len(phLine) > 0:
     finalId = phLine[0][0] 
     ok = False
     i = 0
     myId = -1

     while i < len(phLine) and phLine[i][0] == finalId: 
       if(lookupTable[phLine[i][1]]!=myId):
         myId = lookupTable[phLine[i][1]]
         if(ok):  
           compoundLine += "};\n"
           geoFile.write(compoundLine)
         compoundLine = "Compound Line(" + str(lId) + ") = {"
         j = 0 
         while j < len(idList):
          if idList[j][0]==finalId:
           break
          j+=1
         if j==len(idList):
          idList.append([finalId])
         idList[j].append(lId)
         lId+=1
       if(compoundLine[len(compoundLine)-1] == '{'):
         compoundLine += str(phLine[i][1])
       else:
         compoundLine += ", " + str(phLine[i][1])
       ok = True
       phLine.remove(phLine[i])
     compoundLine += "};\n"
     geoFile.write(compoundLine) 
   
   # After having grouped the lines in as few compound lines as possible, we're writing the ids:
   
   for physicalLine in idList:
     geoFile.write("Physical Line(%d)={%d" %(physicalLine[0],physicalLine[1]))
     i = 2
     while i<len(physicalLine):
      geoFile.write(", %d" %(physicalLine[i]))
      i+=1
     geoFile.write("};\n")
  
   planeSurface+="};\n";
   geoFile.write(planeSurface)
   geoFile.write("Compound Surface(2)={1};\n")
   geoFile.write("Physical Surface(3)={2};\n")
   geoFile.write("//Set some options for better png output\n")
   geoFile.write("General.Color.Background = {255,255,255};\n")
   geoFile.write("General.Color.BackgroundGradient = {255,255,255};\n")
   geoFile.write("General.Color.Foreground = Black;\n")
   geoFile.write("Mesh.Color.Lines = {0,0,0}; \n")
   geoFile.close()
   print ".geo file written successfully"
   
def main():
	if len(sys.argv)!=3:
		usage()
		sys.exit()
	inFile = sys.argv[1]
	outFile = sys.argv[2]
	shape1 = shapefile.Reader(inFile)
	export(shape1, outFile)

if __name__ == '__main__':
  main()



 
