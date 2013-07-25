import numpy as np

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

from subprocess import call
import sys
import shapefile
import os

class Commands( object ):
  def sysArgs( self ):
    self.outfile = self.ArgList.pop()
    while len(self.ArgList)>0:
      carg = self.ArgList.pop(0)
      eval(self.commands[carg])

  #def help_func( self ):
  #  print self.commands
  def gauss_set( self ):
    #form "(cont,a,b,mean,std),..."
    gausStr = self.ArgList.pop(0)
    gausStr = gausStr.split(')')
    gausStr[0] = ' '+gausStr[0]
    gausStr = map(lambda x: x[2:],gausStr)
    gausStr.pop()
    for i in range(len(gausStr)):
      self.f_add()
    gausStr = map(lambda x: x.split(','), gausStr)
    self.Guass = map(lambda x: map(lambda y: float(y), x), gausStr)   
  def sinx_set( self ):
    #form "(cont,w,phi),..."
    sinxStr = self.ArgList.pop(0)
    sinxStr = sinxStr.split(')')
    sinxStr[0] = ' '+sinxStr[0]
    sinxStr = map(lambda x: x[2:],sinxStr)
    sinxStr.pop()
    for i in range(len(sinxStr)):
      self.f_add()
    sinxStr = map(lambda x: x.split(','), sinxStr)
    self.Sinx = map(lambda x: map(lambda y: float(y), x), sinxStr)
  def siny_set( self ):
        #form "(cont,w,phi),..."
    sinyStr = self.ArgList.pop(0)
    sinyStr = sinyStr.split(')')
    sinyStr[0] = ' '+sinyStr[0]
    sinyStr = map(lambda x: x[2:],sinyStr)
    sinyStr.pop()
    for i in range(len(sinyStr)):
      self.f_add()
    sinyStr = map(lambda x: x.split(','), sinyStr)
    self.Siny = map(lambda x: map(lambda y: float(y), x), sinyStr)
  def lon_set( self ):
        #form "(cont,a),..."
    lonStr = self.ArgList.pop(0)
    lonStr = lonStr.split(')')
    lonStr[0] = ' '+lonStr[0]
    lonStr = map(lambda x: x[2:],lonStr)
    lonStr.pop()
    for i in range(len(lonStr)):
      self.f_add()
    lonStr = map(lambda x: x.split(','), lonStr)
    self.Lon = map(lambda x: map(lambda y: float(y), x), lonStr)
  def lat_set( self ):
        #form "(cont,a),..."
    latStr = self.ArgList.pop(0)
    latStr = latStr.split(')')
    latStr[0] = ' '+latStr[0]
    latStr = map(lambda x: x[2:],latStr)
    latStr.pop()
    for i in range(len(latStr)):
      self.f_add()
    latStr = map(lambda x: x.split(','), latStr)
    self.Lat = map(lambda x: map(lambda y: float(y), x), latStr)
  def sinxy( self ):
        #form "(cont,w,u,phi,psi),..."
    sinxyStr = self.ArgList.pop(0)
    sinxyStr = sinxyStr.split(')')
    sinxyStr[0] = ' '+sinxyStr[0]
    sinxyStr = map(lambda x: x[2:],sinxyStr)
    sinxyStr.pop()
    for i in range(len(sinxyStr)):
      self.f_add()
    sinxyStr = map(lambda x: x.split(','), sinxyStr)
    self.Sinxy = map(lambda x: map(lambda y: float(y), x), sinxyStr)
  def f_add( self ):
    self.filelist += [self.f_base+str(self.f_no)]
    self.f_no += 1
  def shortern_func( self ):
    pass
  def load_set( self ):
    self.Load = True
  def anls_set( self ):
    #form "(cont,a,b,mean,std),..."
    anlsStr = self.ArgList.pop(0)
    anlsStr = anlsStr.split(')')
    anlsStr[0] = anlsStr[0][1:]
    anlsStr[1:] = anlsStr[1:][2:]
    for i in range(len(anlsStr)):
      self.f_add()
    anlsStr = map(lambda x: x.split(','), anlsStr)
    self.Annulus = map(lambda x: map(lambda y: float(y), x), anlsStr)
  def join_set( self ):
    self.Join = True

class NcGenerate( object ):

  def nc_generate( self ):

    file_insts = map(lambda x: open(x+'.xyz','w'), self.filelist)

    lrud = [np.min(map(lambda x: x[0],self.Lon)), \
    np.max(map(lambda x: x[0],self.Lon)),             \
    np.min(map(lambda x: x[0],self.Lat)),             \
    np.max(map(lambda x: x[0],self.Lat))]
    print lrud

    for x in np.linspace(lrud[0]-1.0, lrud[1]+1.0,num=(lrud[1]-lrud[0])/0.1):
      for y in np.linspace(lrud[2]-1.0, lrud[3]+1.0,num=(lrud[3]-lrud[2])/0.1):
        insts_no = 0
        for tup in self.Guass:
          file_insts[insts_no].write(str(x)+'\t'+str(y)+'\t'+str(self.gausian( x, y, tup))+'\n')
          insts_no += 1
        for tup in self.Sinx:
          file_insts[insts_no].write(str(x)+'\t'+str(y)+'\t'+str(self.sinx( x, tup))+'\n')
          insts_no += 1
        for tup in self.Siny:
          file_insts[insts_no].write(str(x)+'\t'+str(y)+'\t'+str(self.siny( y, tup))+'\n')
          insts_no += 1
        for tup in self.Sinxy:
          file_insts[insts_no].write(str(x)+'\t'+str(y)+'\t'+str(self.sinxy( x, y, tup))+'\n')
          insts_no += 1
        for tup in self.Lon:
          file_insts[insts_no].write(str(x)+'\t'+str(y)+'\t'+str(self.lon( x, tup))+'\n')
          insts_no += 1
        for tup in self.Lat:
          file_insts[insts_no].write(str(x)+'\t'+str(y)+'\t'+str(self.lat( y, tup))+'\n')
          insts_no += 1
        for tup in self.Annulus:
          file_insts[insts_no].write(str(x)+'\t'+str(y)+'\t'+str(self.annulus( x, y, tup))+'\n')
          insts_no += 1

    map(lambda x: x.close(), file_insts)
    map(lambda x: call(["GMT","surface", x+".xyz", '-G'+x+".nc", "-I0.1/0.1", "-Rd"+str(lrud[0]-1.0)+"/"+str(lrud[1]+1.0)+"/"+str(lrud[2]-1.0)+"/"+str(lrud[3]+1.0)]), self.filelist)

    call(["rm","-f"]+map(lambda x: x+".xyz", self.filelist))
  
  def gausian( self, x, y, tup ):
    r = np.sqrt((x-tup[1])**2 + (y-tup[2])**2)
    mean = tup[3]
    std = tup[4]
    return (100.0/(std*np.sqrt(2.0*np.pi)))*np.exp(-0.5*((r-mean)/std)**2)
  def sinx( self, x, tup):
    return np.sin(float(tup[1])*x*(np.pi/180.)+tup[2])
  def siny( self, y, tup ):
    return np.sin(float(tup[1])*y*(np.pi/180.)+tup[2])
  def sinxy( self, x, y, tup ):
    zx = np.sin(float(tup[1])*x*(np.pi/180.)+tup[3])
    zy = np.sin(float(tup[2])*y*(np.pi/180.)+tup[4])
    return 0.5-abs(zx*zy)
  def lon( self, x, tup ):
    return tup[1]*x
  def lat( self, y, tup ):
    return tup[1]*y
  def annulus( self, x, y, tup ): #ignore
    r = np.sqrt((x-tup[1])**2 + (y-tup[2])**2)
    mean = tup[3]
    std = tup[4]
    return (1.0/(std*np.sqrt(2.0*np.pi)))*np.exp(-0.5*((r-mean)/std)**2)

class ShpGenerate( object ):
  
  def shp_generate( self ):
    
    insts_no = 0
    for tup in self.Guass:
      self.contourmap[insts_no] = tup[0]
      insts_no += 1
    for tup in self.Sinx:
      self.contourmap[insts_no] = tup[0]
      insts_no += 1
    for tup in self.Siny:
      self.contourmap[insts_no] = tup[0]
      insts_no += 1
    for tup in self.Sinxy:
      self.contourmap[insts_no] = tup[0]
      insts_no += 1
    for tup in self.Lon:
      self.contourmap[insts_no] = tup[0]
      self.lonlatfiles += [insts_no]
      insts_no += 1
    for tup in self.Lat:
      self.contourmap[insts_no] = tup[0]
      self.lonlatfiles += [insts_no]
      insts_no += 1
    for tup in self.Annulus:
      self.contourmap[insts_no] = tup[0]
      insts_no += 1    

    map(lambda i: \
    call(["gdal_contour","-fl",str(self.contourmap[i]),str(self.filelist[i])+'.nc',str(self.filelist[i])+'cont.shp']), \
    range(len(self.filelist)))

  def shp_join( self ):
    self.shp_read()
    sf = shapefile.Writer(shapefile.POLYGON)
    sf.poly(parts=self.shp_ins)
    sf.field('id','C','0')
    sf.record('First','Polygon')
    sf.save(str(self.outfile))

  def shp_read( self ):
    self.shp_ins = map(lambda x: shapefile.Reader(x+'cont.shp'),self.filelist)
    print self.shp_ins
    self.shp_ins = map(lambda x: x.shapes(), self.shp_ins)
    print self.shp_ins
    self.shp_ins = map(lambda x: x[0].points, self.shp_ins)
    if self.Join:
      self.join_lonlat()

  def join_lonlat( self ):
    #lonlat = []
    self.lonlatfiles.sort()
    count = 0
    for i in self.lonlatfiles:
      #lonlat += self.shp_ins[i]
      del self.shp_ins[i - count] #order!
      count += 1
    lrud = [np.min(map(lambda x: x[0],self.Lon)), \
    np.max(map(lambda x: x[0],self.Lon)),             \
    np.min(map(lambda x: x[0],self.Lat)),             \
    np.max(map(lambda x: x[0],self.Lat))]
    print lrud
    bbx = [[lrud[0],lrud[2]],[lrud[0],lrud[3]],[lrud[1],lrud[3]],[lrud[1],lrud[2]]]
    self.shp_ins = [bbx] + self.shp_ins

class Main( Commands, NcGenerate, ShpGenerate ):

  outfile    = None
  f_no       = 0
  f_base     = 'generate_field_file'
  filelist   = []
  shp_ins    = []
  contourmap = {}
  ArgList    = []
  Guass      = []
  Sinx       = []
  Siny       = []
  Lon        = []
  Lat        = []
  Sinxy      = []
  Load       = False
  Join       = False
  Annulus    = []
  lonlatfiles= []

  commands = {                  \
  '--guass':'self.gauss_set()' ,\
  '--sinx':'self.sinx_set()'   ,\
  '--siny':'self.siny_set()'   ,\
  '-h':'self.help_func()'      ,\
  '-s':'self.shortern_func()'  ,\
  '--help':'self.help_func()'  ,\
  '--lon':'self.lon_set()'     ,\
  '--lat':'self.lat_set()'     ,\
  '--load':'self.load_set()'   ,\
  '--anuls':'self.anls_set()'  ,\
  '--join':'self.join_set()'   ,\
  '--sinxy':'self.sinxy_set()'  \
  }


  def help_func( self ):
    print '''

    Usage: python generate_field_xyz_data.py [commands] <OutputFileName.shp>

    --guass      Netcdf with gaussian Distribution/circular contour
                 form: (contour,x position,y position,mean,standard deviation)
    -h/--help    displays this message
    --join       joins lon/lat lines to form single shape
    --lat        Netsdf with linear gradient/lattitude contour
                 form: (contour,gradient)
    --lon        Netsdf with linear gradient/longitude contour
                 form: (contour,gradient)
    --load       loads output shapefile to qgis
    --sinx       sin(x)
                 form: (contour,frequency,phase)
    --siny       sin(y)
                 form: (contour,frequency,phase)
    --sinxy      0.5 - sin(x)*sin(y)
                 form: (contour,x frequency,y frequency,x phase,y phase)

    '''

  def run( self ):
    os.system('touch generate_field_file0cont')
    os.system('rm generate_field_file*cont*')
    self.sysArgs()
    self.nc_generate()
    self.shp_generate()
    self.shp_join()
    if self.Load:
      os.system('qgis '+str(self.outfile))

  def sysArgs( self ):
    Commands.sysArgs( self )
  def gauss_set( self ):
    Commands.gauss_set( self )
  def sinx_set( self ):
    Commands.sinx_set( self )
  def siny_set( self ):
    Commands.siny_set( self )
  def Lon_set( self ):
    Commands.Lon_set( self )
  def Lat_set( self ):
    Commands.Lat_set( self )
  def sinxy( self ):
    Commands.sinxy( self )
  def f_add( self ):
    Commands.f_add( self )
  def shortern_func( self ):
    Commands.shortern_func( self )
  def load_set( self ):
    Commands.load_set( self )
  def anls_set( self ):
    Commands.anls_set( self )

  def nc_generate( self ):
    NcGenerate.nc_generate( self )
  def gausian( self, x, y, tup):
    return NcGenerate.gausian( self, x, y, tup)
  def sinx( self, x, tup):
    return NcGenerate.sinx( self, x, tup)
  def siny( self, y, tup ):
    return NcGenerate.siny( self, y, tup )
  def sinxy( self, x, y, tup ):
    return NcGenerate.sinxy( self, x, y, tup )
  def lon( self, x, tup ):
    return NcGenerate.lon( self, x, tup )
  def lat( self, y, tup ):
    return NcGenerate.lat( self, y, tup )
  def annulus( self, x, y, tup ):
    return NcGenerate.annulus( self, x, y, tup)

  def shp_generate( self ):
    ShpGenerate.shp_generate( self )
  def shp_join( self ):
    ShpGenerate.shp_join( self )
  def shp_read( self ):
    ShpGenerate.shp_read( self )

if __name__ == '__main__':
  dlg = Main()
  dlg.ArgList = sys.argv[1:]
  dlg.run()
