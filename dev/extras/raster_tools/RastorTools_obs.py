x = []

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

y = []
lon = []
lat = []
psi = []
inpt = '/home/eml11/plugins_in_progress/wider_area_bathymetry_filtered_subsampled.nc' # testing variable to be removed
outpt = '/home/eml11/plugins_in_progress/new_file005' # testing variable to be removed 

import numpy as np
import copy
import sys
import os
from Scientific.IO import NetCDF
#import gdal_calc

def test(): # testing function to be removed
	global x
	global y
	x = np.array([1,2,3,4,5,6,7,8,9,10])
	y = x**2
	return x, y


def getField(netcdf_file): #obs
	file = NetCDF.NetCDFFile(netcdf_file, 'r')
	global lon, lat, psi
	lon = file.variables['lon'][:]
	lat = file.variables['lat'][:]
	psi = file.variables['z'][:, :]
	lon = np.array(lon)
	lat = np.array(lat)
	psi = np.array(psi)
	return lon, lat, psi

def lon(nc_f):   return nc_f[0]
def lat(nc_f):   return nc_f[1]
def field(nc_f): return nc_f[2]

getField(inpt)

def diferentialOp(field, withRespectTo):
	lim = 'lim'
	result = []
	for i in range(field.size):
		if i > 0 and i < (field.size-1):
			del_field = (field[i+1]-field[i-1])/2.0
			del_par   = (withRespectTo[i+1]-withRespectTo[i-1])/2.0
		elif i == 0:
			del_field = (field[1]-field[0])/2.0
			del_par   = (withRespectTo[1]-withRespectTo[0])/2.0
		else:
			del_field = (field[i]-field[i-1])/2.0
			del_par   = (withRespectTo[i]-withRespectTo[i-1])/2.0
		if isinstance(field, float) == True:# is this field correct param
			if del_par != 0:
				dif_field = del_field/del_par
			else:
				dif_field = lim
		else:
			dif_field = []
			shp = del_field.shape
			for j in range(del_field.size):
				if del_par.flat[j] != 0:
					elementIn_dif_field = del_field.flat[j]/del_par.flat[j]
				else:
					elementIn_dif_field = lim
				dif_field.append(elementIn_dif_field)
			dif_field = np.array(dif_field)
			dif_field.shape = shp
		result.append(dif_field) # note dif_field is an array
	result = np.array(result)
	test_result = copy.copy(result)
	for k in range(result.size):
		if test_result.flat[k] == lim:
			test_result.flat[k] = 0
	test_result = test_result.astype(float)
	test_result *= test_result	
	mx = test_result.max()
	for k in range(result.size):
		if result.flat[k] == lim:
			result.flat[k] = 10*mx
	for i in result.flat:
		i = np.float64(i)
	return result

def diflon(psi = psi,lon = lon):
	for i in range(psi.shape[0]):
		result = diferentialOp(psi[i], lon)
	return result

def diflat(psi = psi,lat = lat):
	psi = psi.transpose()
	for i in range(psi.shape[0]):
		result = diferentialOp(psi[i],lat)
	return result

def DivergenceOfField(psi = psi, lat = lat, lon = lon)
	ddlon = diflon(psi,lon)
	ddlat = diflat(psi,lat)
	result = zeros((ddlat.size, ddlon.size))
	for i in range(lat.size):
		for j in range(lon.size):
			result[i][j] = diflon[i]		

def intOp(field, withRespectTo, c = 0.0):
	result = []
	shp = field.shape
	int_field = np.array([c])
	for i in range(field.size): # note will not work for multidimentional arrays
		if i > 0 and i < (field.size - 1): # note this will not work for multidimentional arrays
			av_field1 = (3*field[i]+field[i-1])
			av_field2 = (3*field[i]+field[i+1])
			del_par1  = (withRespectTo[i]-withRespectTo[i-1])
			del_par2  = (withRespectTo[i+1]-withRespectTo[i])
		elif i == 0:
			av_field1 = (field[1]+3*field[0])
			av_field2 = av_field1
			del_par1  = (withRespectTo[1]-withRespectTo[0])
			del_par2  = del_par1
		else:
			av_field1 = (3*field[i]+field[i-1]) #note maybe inacurate
			av_field2 = av_field1
			del_par1  = (withRespectTo[i]-withRespectTo[i-1])
			del_par2  = del_par1
		int_field += (av_field1*del_par1+av_field2*del_par2)/8.0
		result.append(copy.copy(int_field)) # note int_field can be an array
	result = np.array(result)
	result.shape = shp
	#result += c
	return result

#def advcCalc(inputFileName, outputFileName, function):
	#gdal_calc -A inputFileName --calc function --outfile outputFileName



def returnField(outputFileName):	#obbs
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


