"""
Open .msh on the plane and projects it on to the sphere.
Needs catches for data that's not lon/lat.

@param 	filename: the .msh file created by the plugin on a planar surface.
@return			: the name of the new .msh file that's created. It is the filename with '_Spherical.msh' appended.
"""

from math import *
radEarth = 6.37101e+06

def flat_mesh_spherical (filename):

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
		xyzList = []

		for i in range(numNodes):
			"""
			If wanting to use ellipse rather than sphere replace radEarth with Rn using the following code:

			Equations taken from: http://agamenon.tsc.uah.es/Asignaturas/it/rd/apuntes/RxControl_Manual.pdf.

			Rather than radius of Earth use Rn which is the elliptic Earth and defined by:
			Rn = a / sqrt(1 - (e^2 * sin^2 (lat))

			f = 1 / 298257223563
			eSqrd = (2*f) - (f**2)
			Rn = radEarth / sqrt(1 - (eSqrd * (sin (lat))**2))
			"""

			lon = coordsList[i][0] * pi/180
			lat = coordsList[i][1] * pi/180

			x = radEarth * cos(lon) * cos(lat)
			y = radEarth * sin(lon) * cos(lat)
			z = radEarth * sin(lat)
	
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
				string = string.replace('2 2 1 1', '2 2 3 2')
				msh.write(string)
		
		msh.close()

	lines, numNodes = getLinesNumNodes(filename)
	getLatLon = getLatLon(lines, numNodes)
	xyz = convertLLXYZ(getLatLon, numNodes)

	if '_idBoundary.msh' in filename:
		output = filename.replace('_idBoundary.msh', '_idBoundary_Spherical.msh')

	else:
		output = 'spherical.msh'

	writeMsh(xyz, output, lines)

	return output
