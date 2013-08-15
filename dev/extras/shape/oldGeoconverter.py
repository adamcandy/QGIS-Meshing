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

import sys

threshold = 1

def getPointsList(filename):
	bounds = shapefile.Reader(filename)
	shapes = bounds.shapes()
	for shape in shapes :
		points = shape.points
		splitPoints = shape.parts
		pointsList = []
		for i in range(len(splitPoints)-1):
			pList = points[splitPoints[i]:splitPoints[i+1]]
			if len(pList)>2 and Polygon(pList).area>threshold:
				pointsList.append(pList)

#		if (len(pointsList[len(pointsList)-1]))<=2 or Polygon(pointsList[len(pointsList)-1]).area<=threshold:
#			pointsList = pointsList[0:len(pointsList)-2]
	"""
	for i in range(len(shapes)):
		pointsList.append(shapes[i].points)

			i +=1
			target.write('Point(%d) = {%f, %f, 0, 1.0};\n' %(i, p[0], p[1]))
		# Write the lines connecting the sequential points.
	i=0
	c = 0
	surface = "Plane Surface(1) = {"
	for k in range(len(coords)):

		i+=1
		lineloop = "Line Loop(%d) = {" % i
		if len(l) > 1 :
			for j in range(len(l)-1) :
				target.write("Line(%d) = {%d,%d};\n"%((j+c+1),(c+j+1),(j+c+2)))
				lineloop = lineloop + str(j+c+1) + ", "
			target.write("Line(%d) = {%d,%d};\n"%((c+len(l)),(c+ len(l)),(c+1)))

			target.write(lineloop)
			surface = surface + str(i) + ", "
		c+=len(l)
	if len(surface)!= 20 : surface = surface[0:len(surface)-2]
	surface = surface + "};\n"
	target.write(surface)
	target.close()

print("Writing the file")
readPath = sys.argv[1]
writePath = sys.argv[2]
write_geo(getPointsList(readPath), writePath)
print("File has been written")
