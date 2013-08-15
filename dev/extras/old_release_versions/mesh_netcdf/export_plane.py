from PyQt4.QtCore import * 

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

from PyQt4.QtGui import *
from qgis.core import *

def export(shpFile ,filePath):
	# The function exports the shp file to a .geo. If there isn't any .shp file created, the user will be promped an error.
	geoFile =  open(filePath + ".geo","w")
	shapes =  shpFile.shapes()
	records = shpFile.records()
	pId = 1
	lId = 1
	zCoord = 0
	meshSize = 0.2
	phLine = []
	geoFile.write("zCoord = %f;\n" %zCoord)
	geoFile.write("meshSize = %f;\n" %meshSize)
	# First of all, we'll remove the duplicates
	for i in range(len(shapes)):
		for j in range(len(shapes[i].points)-1):
			while j < len(shapes[i].points)-1 and shapes[i].points[j] == shapes[i].points[j+1]:
				trash = shapes[i].points.pop(j+1)
		trash = shapes[i].points.pop()
	i = 0
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
	pId = 1
	lId = 1
	# This for-loop writes the lines of the file. Each geometric shape (boundary and island) will get an extra edge to close its poligon.
	i = 0
	lLoopId = 1
	#print records
	planeSurface= "Plane Surface(1)={1"
	while i < len(shapes):
		init = pId
		polyId = records[i][1]
		lLoop = "Line Loop(" + str(lLoopId) + ") = {"
		while(i<len(shapes) and polyId == records[i][1]):
			shape = shapes[i]
			#print len(shape.points)
			for j in range(len(shape.points)):
				if j==len(shape.points)-1 and (i==len(shapes)-1 or polyId!=records[i+1][1]):
					geoFile.write("Line(%d) = {%d, %d};\n" %(lId ,pId, init))
					lLoop += str(lId) + "};\n"
					phLine.append((int(records[i][0]),lId))
				else:
					geoFile.write("Line(%d) = {%d, %d};\n" %(lId, pId, pId+1))
					lLoop += str(lId) + ", "
					phLine.append((int(records[i][0]),lId))
				lId+=1
				pId+=1
			i+=1

		geoFile.write(lLoop)
		if lLoopId>1:
			planeSurface += ", " + str(lLoopId)
		lLoopId+=1
	planeSurface += "};\n"
	geoFile.write(planeSurface)
	# The boundary can be splitted into many different shapes. That's why, the first line loop will contain only the boundary, regardless of how many shape it may encapsulate.
	# Puts ths ids in the file as physical lines.
	# How it works: Takes the first element's id, passes it into the file as the id of a physical line and loops through the entire array, searching for lines with the same id. The lines that are found are added to that specific physical line and are deleted from the phLine array. All this stops when phLine will be empty.
	pids = ""
	while len(phLine) > 0:  
		finalId = phLine[0][0] 
		ok = False
		geoFile.write("Physical Line(%d) = {" %finalId)
		i = 0 
		while i < len(phLine):
			if phLine[i][0] == finalId:
				if ok:
					pids+=", "
					geoFile.write(", ")
				ok = True
				pids+=str(phLine[i][1])
				geoFile.write(str(phLine[i][1]))
				phLine.remove(phLine[i])
				continue
			i+=1   
		geoFile.write("};\n")
		geoFile.write("Physical Surface(1)={1};\n")
	geoFile.close()
	return pids
