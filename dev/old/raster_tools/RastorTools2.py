from StandardModules import *
import FileOperations
import MathOperations

#general note: may change variable names to make processes clearer

class fileOp: #check syntax
	def getField(self, netcdf_file): 
		FileOperations.getField(netcdf_file)
	def returnNetCDF(self, inputFileName, outputFileName, outField): 
		FileOperations.returnNetCDF( inputFileName, outputFileName, outField)

class mathOp:
	def division(self, arr1, arr2):
		MathOperations.division(sarr1, arr2):
	def resolveLim(self, arr):
		MathOperations.resolveLim(arr):
	def diferentialOp(self, field, withRespectTo):
		MathOperations.diferentialOp(field, withRespectTo):
	def intOp(self, field, withRespectTo, c = 0.0):
		MathOperations.intOp(sfield, withRespectTo, c = 0.0):
	def f_lon(self, function, psi, lon):
		MathOperations.f_lon(function, psi, lon):
	def f_lat(self, function, psi, lat):
		MathOperations.f_lat(function, psi, lat):
	def divergenceOfField(self, psi, lat, lon):
		MathOperations.divergenceOfField(psi, lat, lon):
	def surfaceIntegral(self, psi, lat, lon):
		MathOperations.surfaceIntegral(psi, lat, lon): 


def lon(nc_f):   return nc_f[0] #potentially obsolete
def lat(nc_f):   return nc_f[1] # --,--
def field(nc_f): return nc_f[2] # --,--

