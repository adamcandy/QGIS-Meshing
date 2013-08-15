
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
Open .msh on the plane and projects it on to the sphere.
Needs catches for data that's not lon/lat.

@param 	filename: the .msh file created by the plugin on a planar surface.
@return			: the name of the new .msh file that's created. It is the filename with '_Spherical.msh' appended.
"""

#needs to be rewritten to work in streographic space rather than lat/lon which it is presumably in now
import numpy as np
from math import *
R = 6.37101e+06

def flat_mesh_spherical ( filename, sterio ):

	def getLinesNumNodes( filename ):

		file = open(filename, 'r')
		lines = file.readlines()
		numNodes = int(lines[4])

		return lines, numNodes

	def getLatLon( line, numNodes ):

		coordsList = []

		for i in range(5, numNodes + 5):
			parts = lines[i].split(' ')
			coordsList.append((float(parts[1]), float(parts[2])))

		return coordsList

	def convertSterio( coordsList, numNodes ):
		#vectorize!!
		u = np.array(map(lambda x: x[0], coordsList))
		v = np.array(map(lambda x: x[1], coordsList))
		lmbd = 4*R**2/(u**2+v**2+4*R**2)#should work as each point is a node rather than coord
		x = lmbd*u
		y = lmbd*v
		z = lmbd*R*(4*R**2-u**2+v**2)

		return zip(x, y, z)

	def convertLLXYZ ( coordsList, numNodes ):
		
		"""
		If wanting to use ellipse rather than sphere replace R with Rn using the following code:

		Equations taken from: http://agamenon.tsc.uah.es/Asignaturas/it/rd/apuntes/RxControl_Manual.pdf.

		Rather than radius of Earth use Rn which is the elliptic Earth and defined by:
		Rn = a / sqrt(1 - (e^2 * sin^2 (lat))

		f = 1 / 298257223563
		eSqrd = (2*f) - (f**2)
		Rn = R / sqrt(1 - (eSqrd * (sin (lat))**2))
		"""

		lon = np.array(map(lambda x: x[0], coordsList)) * pi/180
		lat = np.array(map(lambda x: x[1], coordsList)) * pi/180

		x = R * np.cos(lon) * np.cos(lat)
		y = R * np.sin(lon) * np.cos(lat)
		z = R * np.sin(lat)

		return zip(x, y, z)

	def writeMsh ( xzyList, output, lines ):
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
	if sterio:
		xyz = convertSterio(getLatLon,numNodes)
	else:
		xyz = convertLLXYZ(getLatLon, numNodes)

	if '_idBoundary.msh' in filename:
		output = filename.replace('_idBoundary.msh', '_idBoundary_Spherical.msh')

	else:
		output = 'spherical.msh'

	writeMsh(xyz, output, lines)

	return output
