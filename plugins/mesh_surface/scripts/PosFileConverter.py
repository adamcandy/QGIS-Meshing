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
import NcTools

R = 6.378E6

class converter( NcTools.NcReader): #appears to be writing pos files correctly

  postype = 'SCALARPOINTS'

  def wholeDirect( self, direc, spherical ):
    posTime = datetime.datetime.now()
    print 'Started :'+str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    ncfiles = os.popen("echo "+str(direc)+'*.nc').read().split()
    for f in ncfiles:
      self.singleNetCDFLayerFileName = f
      self.postviewFileName = f[:-2]+'pos'
      print self.singleNetCDFLayerFileName
      print str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
      try:#note not the most efficient way of calling this
        self.writePosFile(spherical)
      except :
        print 'Failed to write'
        continue
    print "done :" + str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    timePassed = datetime.datetime.now() - posTime
    print "Time :" + str(timePassed.seconds) + " seconds."
    
  def _convertSpherical( self ):
    #assume x0, y0 co-ordinates in stereographic using gdal
    l = 4*R**2/(self.x0**2+self.x1**2+4*R**2)
    self.phi = self.phi/l

  def _writeFunc( self ):#alter to primerily call quad
    f = open(str(self.postviewFileName),'w')
    f.write("""View "background_edgelength" {\n""")
    print 'ASC', self.x0.flatten()
    print 'ASC', self.x1.flatten()
    print 'ASC', self.phi.flatten()
    if self.postype == 'SCALARPOINTS':
      self._writeLines(f,self.x0.flatten(),self.x1.flatten(),self.phi.flatten())
    elif self.postype == 'SCALARQUADS':
      self.write_quadrangle(f)
    f.write('};')
    f.close()
    
  _writeLines = vectorize(lambda f, x, y, z: f.write("SP("+str(x)+","+str(y)+",0){"+str(z)+"};\n"))
  
  def write_quadrangle( self, f ):
    x0 = self.x0[:-1,:-1]; x1 = self.x1[:-1,:-1]
    x0_s = roll(self.x0,-1,axis=1)[:-1,:-1]; x1_s = roll(self.x1,-1,axis=0)[:-1,:-1]
    
    phi01 = self.phi[:-1,:-1]
    phi0_s1 = roll(self.phi,-1,axis=1)[:-1,:-1]
    phi0_s1_s = roll(roll(self.phi,-1,axis=0),-1,axis=1)[:-1,:-1]
    phi01_s = roll(self.phi,-1,axis=0)[:-1,:-1]
    
    x0 = x0.flatten(); x1 = x1.flatten()
    x0_s = x0_s.flatten(); x1_s = x1_s.flatten()
    phi01 = phi01.flatten(); phi0_s1 = phi0_s1.flatten() 
    phi0_s1_s = phi0_s1_s.flatten(); phi01_s = phi01_s.flatten()
    
    #this is incorrect: not obteining quadrangle verteses
    r = range(len(x0)-1) # is this correct, where do the rolled doubles end up?
    
    map(lambda i:                             \
    f.write("SQ(" +                           \
    str(x0[i])+","+str(x1[i])+",0," +         \
    str(x0_s[i])+","+str(x1[i])+",0," +       \
    str(x0_s[i])+","+str(x1_s[i])+",0," +     \
    str(x0[i])+","+str(x1_s[i])+",0){" +      \
    str(phi01[i])+","+str(phi0_s1[i])+"," +   \
    str(phi0_s1_s[i])+","+str(phi01_s[i]) +   \
    "};\n"),                                  \
    r)
    
  def _read_nc( self ):
    NcTools.NcReader._read_nc( self )
  def _read_nc_xyrange( self ):
    NcTools.NcReader._read_nc_xyrange( self )
  def _read_nc_xy( self ):
    NcTools.NcReader._read_nc_xy( self )
  def _ReadFunc( self ):
    NcTools.NcReader.ReadFunc( self )
    
  def writePosFile( self , spherical = False):    #find some algarithm to decide what to return for the 0 value
    print "Writing PostView File..."
    
    # Check the file variables so that the appropriate function can be called.
    self.ncFile = self.singleNetCDFLayerFileName
    self._ReadFunc()
    if spherical:
      self._convertSpherical()
    self._writeFunc()
    print "PostView File Written."
    


if __name__ == '__main__':
  import sys
  if len(sys.argv) == 1:
    arg = os.path.realpath(__name__)[:-8]
  elif len(sys.argv) == 2:
    arg = sys.argv[1]
    sph = False
  else:
    arg = sys.argv[1]
    sph = sys.argv[2]
  converter().wholeDirect(str(arg), sph)
  

