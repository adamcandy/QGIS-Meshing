from input_output_for_id import getShapeData,saveShapeFile

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

class DefineDomain(object):
	def define_bounds(self, isIdLayer):   
		print "defining id's"

		self.domainPoints, self.domainRecords, self.boundaryPoints, self.boundaryRecords = getShapeData(self.domainShapefileLayerFileName, self.idFilePath, self.threshold)

		self.boundaryIds, self.bounds = assignIDs(self.domainPoints, self.boundaryPoints, self.defID, self.domainRecords, self.boundaryRecords, isIdLayer).result

		self.bounds = connectLines(self.bounds)
		print "done defining id's"
