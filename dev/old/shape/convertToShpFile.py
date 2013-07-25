#imports the library shapefile to allow the shapefile operations

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

readPath = "p.shp"
writePath = "w.shp"




line = "Point(2) = {1,2,3,4}"

tokens = parsePoint(line)

for t in tokens:
	print t + " "


"""
read = open(readPath,"r")
write = shapefile.Editor(shapefile=writePath) 

while 1 : 


	line = f.readline()
	if not line :
		print 'end of file'
		break
	points = parsePoint(line)
	writePointToFile(points,write)

	print 'written to file  --> '
	print line

read.close()
write.close()

"""

def writePointToFile(points,fileStream):
	f = shapefile.Editor(shapefile=fp)
	fileStream.point(float(points[0]),float(points[1]),float(points[2]),float(points[3]))
	fileStream.record("Appended","Point")
	fileStream.save(fp)
	return


def parsePoint(line):
	if 'Point' in line :
		tokens = line.split('= {',2)
	  points = tokens[1].split(', ',4)
		points[3] = points[3][0:len(points[3])-3]
		return points
