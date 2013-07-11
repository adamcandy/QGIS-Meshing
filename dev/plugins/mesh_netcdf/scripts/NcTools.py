#! /bin/python

'''
Read-Write for NetCDF,
Based on Scientific.IO
'''

#at some point add in code for gdal layers to make it compatible in qgis

from Scientific.IO import NetCDF
import numpy as np
import osgeo.gdal as gdal
import os

class UnsuportedRasterVariableError(Exception): #note this is in Error checks somewhere
  def __init__(self, variableNames):
    print 'file Variables', variableNames, 'not supported'

class NcReader( object ):
      
  # Lon-lat.
  def _read_nc( self ):
    lon = self.fnc.variables['lon'][:]
    lat = self.fnc.variables['lat'][:] 
    field = self.fnc.variables['z'][:, :]
    field = np.abs(np.where(field == 0, 0.1, field))
  
    self.x0 = np.outer(np.ones_like(lat),lon)
    self.x1 = np.outer(lat, np.ones_like(lon))
    self.phi = field


  # X/Y range.
  def _read_nc_xyrange( self ): #still does not seem to be working
    xs = self.fnc.variables['x_range']
    ys = self.fnc.variables['y_range']
    space = self.fnc.variables['dimension']
    field = self.fnc.variables['z']
    #field = np.abs(np.where(field == 0, 0.1, field))
  
    xList = np.linspace(xs[0], xs[1], space[0])
    yList = np.linspace(ys[0], ys[1], space[1])
    
    self.x0 = np.outer(np.ones_like(yList),xList).flatten()
    self.x1 = np.outer(yList, np.ones_like(xList)).transpose().flatten()
    self.phi = field
    

  # X-Y.
  def _read_nc_xy( self ):
    x = self.fnc.variables['x'][:]
    y = self.fnc.variables['y'][:]
    field = self.fnc.variables['z'][:, :]
    field = np.abs(np.where(field == 0, 0.1, field))
    
    self.x0 = np.outer(np.ones_like(y),x)
    self.x1 = np.outer(y, np.ones_like(x))
    self.phi = field

  def _read_nc_pam(self):
    # f.open(self.ncFile + '.aux.xml')
    field = self.fnc.variables['Band1'][:, :]
    xlen = field.shape
    # Hard-coded values for now - needs to read PAM metadata
    xList = np.linspace(-16.0, 5.0, xlen[1])
    yList = np.linspace(66, 44, xlen[0])
    # f.close()
    self.x0 = np.outer(np.ones_like(yList),xList).flatten()
    self.x1 = np.outer(yList, np.ones_like(xList)).transpose().flatten()
    self.phi = field
 
  def ReadFunc( self ):
    self.fnc = NetCDF.NetCDFFile(str(self.ncFile), 'r')
    self.variables = self.fnc.variables.keys()
    
    if 'lon' in self.variables:
      self._read_nc()
    elif 'x_range' in self.variables:
      self._read_nc_xyrange()
    elif 'x' in self.variables:
      self._read_nc_xy()
    elif (os.path.exists(self.ncFile + '.aux.xml')):
      self._read_nc_pam()
    else:
      raise UnsuportedRasterVariableError(str(variableNames))#this isn't defined here
      
class NcWriter( object ):
  typ = 'll'
  ncFile = None
  phi = None
  xvar = None
  yvar = None
  
  def __init__( self ):
    isreformat = os.popen('which grdreformat')
    if isreformat.read() == '':
      print 'Warning:  Grd not installed. Netcdf will not be compatible with some programs.'
        
  def listFileTypes( self ):
    print '''
    ll: lonlat
    xy: xy
    xr: xy range
    '''
    
  def _write_nc( self ):
    x = self.fnc.createVariable("lon","d",("dim2",))
    y = self.fnc.createVariable("lat","d",("dim1",))
    z = self.fnc.createVariable("z","d",("dim1","dim2"))
    if self.xvar == None: #note may change for lon-lat
      self.xvar = np.arange(self.phi.shape[1])
    if self.yvar == None:
      self.yvar = np.arange(self.phi.shape[0])
    x.assignValue(self.xvar)
    y.assignValue(self.yvar)
    z.assignValue(self.phi)
    
  def _write_nc_xy( self ):
    x = self.fnc.createVariable("x","d",("dim2",))
    y = self.fnc.createVariable("y","d",("dim1",))
    z = self.fnc.createVariable("z","d",("dim1","dim2"))
    if self.xvar == None:
      self.xvar = np.arange(self.phi.shape[1])
    if self.yvar == None:
      self.yvar = np.arange(self.phi.shape[0])
    x.assignValue(self.xvar)
    y.assignValue(self.yvar)
    z.assignValue(self.phi)
    
  def _write_nc_xyrange( self ):
    self.fnc.createDimension('single',1)
    self.fnc.createDimension('double',2)
    self.fnc.createDimension('field_len',self.phi.size)
    xs = self.fnc.createVariable("x_range","d",("double",))
    ys = self.fnc.createVariable("y_range","d",("double",))
    z = self.fnc.createVariable("z","d",("field_len",))
    space = self.fnc.createVariable('dimension',"i",("single",))
    if self.xvar == None:
      self.xvar = np.arange(self.phi.shape[1])
    if self.yvar == None:
      self.yvar = np.arange(self.phi.shape[0])
    self.phi.flatten()
    xs.assignValue(np.np.array([self.xvar[0],self.xvar[-1]]))
    ys.assignValue(np.np.array([self.yvar[0],self.yvar[-1]]))
    z.assignValue(self.phi)
    space.assignValue(self.xvar[1]-self.xvar[0])
    
  def _genDim( self ):
    a1 = self.phi.shape
    self.fnc.createDimension('dim1',a1[1])
    self.fnc.createDimension('dim2',a1[0])
    
  def WriteFunc( self ):
    if not ('.nc' in self.ncFile):
      self.ncFile = str(self.ncFile)+'.nc'
    self.fnc = NetCDF.NetCDFFile(str(self.ncFile), 'w')
    self._genDim()
    if self.typ == 'll':
      self._write_nc()
    elif self.typ == 'xy':
      self._write_nc_xy()
    elif self.typ == 'xr':
      self._write_nc_xyrange()
    else:
      self.fnc.close()
      self.listFileTypes()
      raise UnsuportedRasterVariableError(str(self.typ))
    self.fnc.close()
    os.system('grdreformat '+str(self.ncFile)+' '+str(self.ncFile))   
    



