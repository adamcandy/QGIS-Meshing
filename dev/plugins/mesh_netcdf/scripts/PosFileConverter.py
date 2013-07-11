"""
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

  def _writeFunc( self ):
    f = open(str(self.postviewFileName),'w')
    f.write("""View "background_edgelength" {\n""")
    print 'ASC', self.x0.flatten()
    print 'ASC', self.x1.flatten()
    print 'ASC', self.phi.flatten()
    self._writeLines(f,self.x0.flatten(),self.x1.flatten(),self.phi.flatten())
    f.write('};')
    f.close()
    
  _writeLines = vectorize(lambda f, x, y, z: f.write("SP("+str(x)+","+str(y)+",0){"+str(z)+"};\n"))
    
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
  

