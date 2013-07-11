from StandardModules import *
import FileOperations
import MathOperations

#general note: may change variable names to make processes clearer

class fileOp:
	def getField(self, netcdf_file):
		self.data = FileOperations.getField(netcdf_file)
		self.lon = self.data[0]
		self.lat = self.data[1]
		self.psi = self.data[2]
	def returnNetCDF(self, inputFileName, outputFileName, outField): 
		FileOperations.returnNetCDF( inputFileName, outputFileName, outField)

class mathOp:
	def division(self, arr1, arr2):
		self.result = MathOperations.division(sarr1, arr2)
	def resolveLim(self, arr):
		self.result = MathOperations.resolveLim(arr)
	def diferentialOp(self, field, withRespectTo):
		self.result = MathOperations.diferentialOp(field, withRespectTo)
	def intOp(self, field, withRespectTo, c = 0.0):
		self.result = MathOperations.intOp(sfield, withRespectTo, c = 0.0)
	def f_lon(self, function, psi, lon):
		self.result = MathOperations.f_lon(function, psi, lon)
	def f_lat(self, function, psi, lat):
		self.result = MathOperations.f_lat(function, psi, lat)
	def divergenceOfField(self, psi, lat, lon):
		self.result = MathOperations.divergenceOfField(psi, lat, lon)
	def surfaceIntegral(self, psi, lat, lon):
		self.result = MathOperations.surfaceIntegral(psi, lat, lon)
	def diferentiateFields(self,Field1, Field2, param1):
		self.result = MathOperations.diferentiateFields(Field1, Field2, param1)
	def intFields(self,Field1, Field2, param1, c=0):
		self.result = MathOperations.intFields(Field1, Field2, param1, c=0)
