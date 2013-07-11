"""
This script produces a shapefile from the gmsh mesh(.msh) file.

"""

import shapefile

"""
The local variable __error_occured is used to track errors within the
script. It stores 1 if any error occured in the script and 0 otherwise
"""
__error_occured = 0

"""
This method removes the new line character from the given line
@param line : specifies the line from which the new line 
							character has to be removed
@return			: returns the line with the new line character removed
"""
def __removeReturnInLine(line):
	if line[len(line)-1]=='\n' :
		line= line[0:-1]
	return line

"""
This method returns the list of the nodes in the .msh file
@param lines : specifies the lines of the .msh file which contains
							 the data about the nodes
@return			 : returns the list of points of the nodes
"""
def __get_nodes(lines):
	nodes = []
	for line in lines :
		pt = line.split()
		try:
			nodes.append([float(pt[1]),float(pt[2]),float(pt[3])])
		except ValueError:
		  __error_occured = 1
		  return []
	return nodes
	
"""
This method returns the points of the connecting triangles for the mesh
@param nodes  : array of points of all the nodes which are used in the
  # run method that performs all the real work
								.msh file
@param points :	array of nodes which are connected to make the 
								current triangle
@return				: returns the points which joins to form the triangle for
								the mesh
"""
def __get_poly_points(nodes,pts):
	try:
		points = [nodes[int(pts[0])-1],nodes[int(pts[1])-1],nodes[int(pts[2])-1],nodes[int(pts[0])-1]]
	except ValueError:
		__error_occured = 1
		return []
	return points

"""
This method returns the points for all the triangles included in the mesh
@param nodes : array of co-ordinates of all the nodes which are 
							 used in the mesh
@param lines : array of the input from the file which contains only
							 the information about each of triangles for the mesh
@return			 : returns the list of points for all the triangles included
							 in the mesh
"""
def getPointsForElements(nodes,lines):
	points = []
	for line in lines:
		try:
			pt = line.split()
			if pt[1]=="2":
				points.append(__get_poly_points(nodes, pt[5:8]))
		except IndexError:
			__error_occured = 1
			return [] 
	return points

"""
This method reads the .msh file and then produces the shapefile for
the .msh file
@param readPath  : specifies the path of the .msh file
@param writePath : specifies the path to which the shapefile has 
									 to be written
"""
def __generate_shp(readPath, writePath):
	try:
		read = open(readPath,"r")
		lines = read.readlines()
	except IOError : 
		__error_occured = 1
		return
	target = shapefile.Writer(shapeType=shapefile.POLYGON)
	for i in range(len(lines)):
		if lines[i]=="":
			__error_occured = 1
			return
		lines[i] = __removeReturnInLine(lines[i])
	nodes = []
	points = []	
	i = 0
	#gets all the nodes from the mesh file
	while i!=len(lines):
		if lines[i]=="$Nodes":
			numberOfNodes= int(lines[i+1])
			nodes = __get_nodes(lines[i+2:i+2+numberOfNodes])
			i += numberOfNodes+3
			break
		i+=1

	#error if the file has no elements, i.e. no information about triangles
	if i==len(lines):
		__error_occured = 1
		return

	#gets all the triangles for the mesh
	while i!=len(lines):
		if lines[i] == "$Elements":
			numberOfElements = int(lines[i+1])
			points = getPointsForElements(nodes,lines[i+2:i+2+numberOfElements])
			i+=numberOfElements+3
			break
		i+=1
	target.poly(parts=points)
	target.field("Mesh","C","40")
	target.record("First", "Polygon")
	try :
		target.save(writePath)
	except IOError:
		__error_occured = 1
		return

"""
This method uses the other auxilary method to generate a shapefile
from the .msh file. This method is the main method for the script
and should be invoked to generate a mesh in a shapefile format.
@param readPath  : specifies the path of the .msh file
@param writePath : specifies the path to which the shapefile generated
									 has to be saved
@return					 : returns the error_occured value for the script

"""
def getShapeForMesh(readPath,writePath):
	__error_occured = 0
	if readPath[len(readPath)-4:len(readPath)]!=".msh":
		__error_occured = 1
	else :
		__generate_shp(readPath,writePath)
		__error_occurred = 1  
	return __error_occured
