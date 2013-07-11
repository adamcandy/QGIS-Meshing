from input_output_for_id import ShapeData
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
