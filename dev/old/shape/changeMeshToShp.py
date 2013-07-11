"""
This script produces a shapefile from the gmsh mesh(.msh) file.

"""

import shapefile
import sys

class Errors: 
	INVALID_MESH_FORMAT = "ERROR: The mesh file given is not in a suitable format. Please provide a mesh file generated using gmsh"
	NO_ELEMENTS_IN_MESH_FILE = "ERROR: The mesh file contains no elements"
	INVALID_EXTENSION = "ERROR: The extentsion of the given mesh file is not valid. Please use a .msh file produced using gmsh"


"""
This method removes the new line character from the given line
@param line : specifies the line from which the new line 
							character has to be removed
@return			: returns the line with the new line character removed
"""
def removeReturnInLine(line):
	if line[len(line)-1]=='\n' :
		line= line[0:-1]
	return line

"""
This method returns the list of the nodes in the .msh file
@param lines : specifies the lines of the .msh file which contains
							 the data about the nodes
@return			 : returns the list of points of the nodes
"""
def getNodes(lines):
	nodes = []
	for line in lines :
		pt = line.split()
		try:
			nodes.append([float(pt[1]),float(pt[2]),float(pt[3])])
		except ValueError:
			print(Errors.INVALID_MESH_FORMAT)
			sys.exit()
	return nodes

	print("Indentifying Nodes...")
"""
This method returns the points of the connecting triangles for the mesh
@param nodes  : array of points of all the nodes which are used in the
								.msh file
@param points :	array of nodes which are connected to make the 
								current triangle
@return				: returns the points which joins to form the triangle for
								the mesh
"""
def getPolyPoints(nodes,pts):
	try:
		points = [nodes[int(pts[0])-1],nodes[int(pts[1])-1],nodes[int(pts[2])-1],nodes[int(pts[0])-1]]
	except ValueError:
		print(Errors.INVALID_MESH_FORMAT)
		sys.exit()
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
				points.append(getPolyPoints(nodes, pt[5:8]))
		except IndexError:
			print(Error.INVALID_MESH_FORMAT)
			sys.exit()
	return points

"""
This method reads the .msh file and then produces the shapefile for
the .msh file
@param readPath  : specifies the path of the .msh file
@param writePath : specifies the path to which the shapefile has 
									 to be written
"""
def generateShp(readPath, writePath):
	try:
		read = open(readPath,"r")
		lines = read.readlines()
	except IOError : 
		print(Errors.INVALID_MESH_FORMAT)
		sys.exit()
	target = shapefile.Writer(shapeType=shapefile.POLYGON)
	for i in range(len(lines)):
		if lines[i]=="":
			print(Errors.INVALID_MESH_FORMAT)
			sys.exit()
		lines[i] = removeReturnInLine(lines[i])
	nodes = []
	points = []	
	i = 0
	while i!=len(lines):
		if lines[i]=="$Nodes":
			numberOfNodes= int(lines[i+1])
			nodes = getNodes(lines[i+2:i+2+numberOfNodes])
			i += numberOfNodes+3
			break
		i+=1
	if i==len(lines):
		print(Errors.NO_ELEMENTS_IN_MESH_FILE)
		sys.exit()

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
		print(Errors.INVALID_WRITE_PATH)
		sys.exit()

"""
This method prints the usage of the script
"""
def usage():
	print("ERROR INCCORECT USAGE\nProgram Usage:\n $ python <NAME OF SCRIPT> <PATH OF .msh FILE> <PATH TO WRITE>")

if len(sys.argv)!=3:
	usage()
	sys.exit()
readPath = sys.argv[1]
writePath = sys.argv[2]
if readPath[len(readPath)-4:len(readPath)]!=".msh":
	print(Errors.INVALID_EXTENSION)
	sys.exit()
generateShp(readPath,writePath)
