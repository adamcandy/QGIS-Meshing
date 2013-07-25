"""

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

Generates a PostView file from a .nc file. The three methods are for three of the
types of coordinate system used in NetCDFs: lat-lon, x-y, and x/y start/stop with x/y step.
"""
import os
from numpy import *
from time import gmtime, strftime, clock
import datetime
from Scientific.IO import NetCDF

class UnsuportedRasterVariableError(Exception):
	def __init__(self, variableNames):
		print 'file Variables', variableNames, 'not supported'

class converter(): #appears to be writing pos files correctly
	def wholeDirect( self, direc ):
		posTime = datetime.datetime.now()
		print 'Started :'+str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
		ncfiles = os.popen("echo "+str(direc)+'*.nc').read().split()
		for f in ncfiles:
			self.singleNetCDFLayerFileName = f
			self.postviewFileName = f[:-2]+'pos'
			print self.singleNetCDFLayerFileName
			print str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
			try:#note not the most efficient way of calling this
				self.writePosFile()
			except :
				print 'Failed to write'
				continue
		print "done :" + str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
		timePassed = datetime.datetime.now() - posTime
		print "Time :" + str(timePassed.seconds) + " seconds."
		
		
	# Lon-lat.
	def _read_nc( self ):
		lon = self.fnc.variables['lon'][:]
		lat = self.fnc.variables['lat'][:] 
		field = self.fnc.variables['z'][:, :]
		field = abs(where(field == 0, 0.1, field))
	
		self.x0 = outer(ones_like(lat),lon).flatten()#may not be the most efficient way of calling this
		self.x1 = outer(lat, ones_like(lon)).flatten()
		self.phi = field.flatten()


	# X/Y range.
	def _read_nc_xyrange( self ): #still does not seem to be working
		xs = self.fnc.variables['x_range']
		ys = self.fnc.variables['y_range']
		space = self.fnc.variables['dimension']
		field = self.fnc.variables['z']
		field = abs(where(field == 0, 0.1, field))
	
		xList = linspace(xs[0], xs[1], space[0])
		yList = linspace(ys[0], ys[1], space[1])
		
		self.x0 = outer(ones_like(yList),xList).flatten()
		self.x1 = outer(yList, ones_like(xList)).transpose().flatten()
		self.phi = field
		

	# X-Y.
	def _read_nc_xy( self ):
		x = self.fnc.variables['x'][:]
		y = self.fnc.variables['y'][:]
		field = self.fnc.variables['z'][:, :]
		field = abs(where(field == 0, 0.1, field))
		
		self.x0 = outer(ones_like(y),x).flatten()
		self.x1 = outer(y, ones_like(x)).flatten()
		self.phi = field.flatten()


	def _writeFunc( self ):
		f = open(str(self.postviewFileName),'w')
		f.write("""View "background_edgelength" {\n""")
		self._writeLines(f,self.x0,self.x1,self.phi)
		f.write('};')
		f.close()
		
	_writeLines = vectorize(lambda f, x, y, z: f.write("SP("+str(x)+","+str(y)+",0){"+str(z)+"};\n"))
		
	def writePosFile( self ):		#find some algarithm to decide what to return for the 0 value
		print "Writing PostView File..."
		
		# Check the file variables so that the appropriate function can be called.
		self.fnc = NetCDF.NetCDFFile(str(self.singleNetCDFLayerFileName), 'r')
		variableNames = self.fnc.variables.keys()
		
		if 'lon' in variableNames:
			self._read_nc()
		elif 'x_range' in variableNames:
			self._read_nc_xyrange()
		elif 'x' in variableNames:
			self._read_nc_xy()
		else:
			raise UnsuportedRasterVariableError(str(variableNames))
			
		self._writeFunc()
		print "PostView File Written."
		


if __name__ == '__main__':
	import sys
	if len(sys.argv) == 1:
		arg = os.path.realpath(__name__)[:-8]
	else:
		arg = sys.argv[1]
		
	converter().wholeDirect(str(arg))
	

