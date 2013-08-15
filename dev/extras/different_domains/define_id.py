from input_output_for_id import ShapeData

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

from define_boundary_id import *

class DefineDomain(assignIDs):
	def define_bounds(self, isIdLayer):   
		print "defining id's"
		
		self.domainData = ShapeData(self.domainShapefileLayerFileName, self.threshold, True)
		if isIdLayer:
			self.boundaryData = ShapeData(self.idFilePath, self.threshold, False)

		self.assignIDsMethod(isIdLayer)
		self.domainData.points = connectLines(self.domainData.points)
		self.toTextFile()
		print "done defining id's"

	def assignIDsMethod(self,ok):
		assignIDs.assignIDsMethod(self,ok)

	def toTextFile(self):
		txt = open('/home/eml11/shapefile_data.txt', 'w')
		txt.write("regionID\n")
		txt.write(str(self.domainData.regionIDs))
		txt.write('\n\nshapes\n')
		txt.write(str(self.domainData.shapes))
		txt.write('\n\nboundaryIDList\n')
		txt.write(str(self.boundaryIDList))
		txt.write('\n\ndomainPoints\n')
		txt.write(str(self.domainData.points))
		txt.close
