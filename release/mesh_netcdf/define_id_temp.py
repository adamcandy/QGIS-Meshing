from input_output_for_id import getShapeData,saveShapeFile
from define_boundary_id import *

class DefineDomain(object):
	def define_bounds(self, isIdLayer):   
		print "defining id's"

		self.domainPoints, self.domainRecords, self.boundaryPoints, self.boundaryRecords = getShapeData(self.domainShapefileLayerFileName, self.idFilePath, self.threshold)

		self.boundaryIds, self.bounds = assignIDs(self.domainPoints, self.boundaryPoints, self.defID, self.domainRecords, self.boundaryRecords, isIdLayer).result

		self.bounds = connectLines(self.bounds)
		print "done defining id's"
