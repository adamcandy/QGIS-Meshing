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

Open .msh on the plane and projects it on to the sphere.
Needs error catches and tidying:
	Automatically append the existing file name so it ends _spherical.msh. 
	Check it is projecting in the correct orintation and isn't upside-down.
"""

from math import sin, cos, pi
radEarth = 6.37101e+06

def getLinesNumNodes(filename):
	file = open(filename, 'r')
	lines = file.readlines()
	numNodes = int(lines[4])
	return lines, numNodes

def getLatLon(line, numNodes):

	coordsList = []

	for i in range(5, numNodes + 5):
		parts = lines[i].split(' ')
		coordsList.append((float(parts[1]), float(parts[2])))

	return coordsList

def convertLLXYZ (coordsList, numNodes):
	"""
	x = radiusOfSphere * cos(longitude * cos(latitude)
	y = radiusOfSphere * -sin(latitude);
	z = radiusOfSphere * sin(longitude) * cos(latitude)
	"""
	xyzList = []

	for i in range(numNodes):
		lon = coordsList[i][0] * pi/180
		lat = coordsList[i][1] * pi/180

		x = radEarth * cos(lon) * cos(lat)
		y = radEarth * -sin(lat)
		z = radEarth * sin(lon) * cos(lat)
	
		xyzList.append((x, y, z))

	return xyzList

def writeMsh (xzyList, output, lines):
	msh = open(output, 'w')

	for i in range(len(lines)):

		if i < 5:
			msh.write(lines[i])

		elif i >= 5 and i <= numNodes + 4:
			string = str(i - 4) + ' ' + str(xzyList[i - 5][0]) + ' ' + str(xzyList[i - 5][1]) + ' ' + str(xzyList[i - 5][2]) + '\n'
			msh.write(string)

		else:
			string = lines[i]
			string = string.replace("2 2 1 1", "2 2 3 2")
			msh.write(string)
		
	msh.close()

lines, numNodes = getLinesNumNodes('ireland_ids_flat.shp.msh')
get = getLatLon(lines, numNodes)
xyz = convertLLXYZ(get, numNodes)
writeMsh(xyz, 'spherical.msh', lines)
