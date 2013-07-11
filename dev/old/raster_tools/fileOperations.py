from StandardModules import *

x   = []
y   = []
lon = []
lat = []
psi = []

def getField(netcdf_file): #edit to accept netCDF with x,y
	DocStrings.i
	file = NetCDF.NetCDFFile(netcdf_file, 'r')
	global lon, lat, psi, x, y
	variableNames = file.variables.keys()
	if lon in variableNames:
		lon = file.variables['lon'][:]
		lat = file.variables['lat'][:]
		psi = file.variables['z'][:, :]
		lon = np.array(lon)
		lat = np.array(lat)
		psi = np.array(psi)
		return lon, lat, psi
	elif x_range in variableNames:
		xMin = file.variables['x_range'][0]; xMax = file.variables['x_range'][1]
		yMin = file.variables['y_range'][0]; yMax = file.variables['y_range'][1]
		xSpace = file.variables['spacing'][0]; ySpace = file.variables['spacing'][1]
		psi = file.variables['z'] #[:, :]?
		x = [xMin]; y = [yMin]; nextx = xMin; nexty = yMin step = 1
		while x <= xMax:
			nextx += step*xSpace
			x += copy.copy(nextx)
		while y <= yMax:
			nexty += step*ySpace
			y += copy.copy(nexty)
		x = np.array(x)
		y = np.array(y)
		psi = np.array(psi)
		return x, y, psi
	else:
		print variableNames, 'not supported'

def returnNetCDF(inputFileName, outputFileName, outField):
	"""incomplete"""
	os.system('gdal_calc.py -A inputFileName --calc 1 --outfile RastorTools_tempFile_returnNetCDF')
	os.system('gdal_calc.py -A Find -name RastorTools_tempFile_returnNetCDF --calc A*%s --outfile 		outputFileName' % str(outField))
	os.system('rm -Find -name RastorTools_tempFile_returnNetCDF')

def returnField(outputFileName):	#potentially obsolete
	output_file = '%s.nc' % str(outputFileName)
	global outLon, outLat, outField, outsize1, outsize2
	f = NetCDF.NetCDFFile(outputFileName, 'w')
	f.createDimension('dim1', outsize1)
	f.createDimension('dim2', outsize2)
	f.createVariable('lon', 'd', ('dim1',))
	f.createVariable('lat', 'd', ('dim2',))
	f.createVariable('z', 'd', ('dim1','dim2',))
	f.variables['lon'][:] = outLon
	f.variables['lat'][:] = outLat
	f.variables['z'][:] = outField
	f.close()
