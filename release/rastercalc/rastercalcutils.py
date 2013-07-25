# -*- coding: utf-8 -*-

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

#******************************************************************************
#
# RasterCalc
# ---------------------------------------------------------
# Raster manipulation plugin.
#
# Based on rewritten rasterlang plugin (C) 2008 by Barry Rowlingson
#
# Copyright (C) 2009 GIS-Lab (http://gis-lab.info) and
# Alexander Bruy (alexander.bruy@gmail.com)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/copyleft/gpl.html>. You can also obtain it by writing
# to the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.
#
#******************************************************************************

from qgis.core import *

from PyQt4.QtCore import *

import numpy
import osgeo.gdal as gdal

rasterList = {}

class Group:
  def __init__( self, layer, label ):
    self.layers = [ layer ]
    self.labels = [ label ]
    e = Extent( layer )
    self.info = "Group: %sx%s" % ( layer.width(), layer.height() )

  def addLayer( self, layer, label ):
    self.layers.append( layer )
    self.labels.append( label )

class GroupedLayers:
  def __init__( self ):
    self.groups = []
    return

  def addLayer( self, layer, label ):
    for group in self.groups:
       if isCompatible( layer, group.layers[ 0 ] ):
         group.addLayer( layer, label )
         return
    newGroup = Group( layer, label )
    self.groups.append( newGroup )
    return

  def findGroup( self, layer ):
    groupIndex = 0
    for group in self.groups:
      for lay in group.layers:
        if lay == layer:
          return groupIndex
      groupIndex = groupIndex + 1
    return None

class Extent:
  def __init__( self, layer ):
    e = layer.extent()
    try:
      self.xmin = e.xMinimum()
      self.ymin = e.yMinimum()
      self.xmax = e.xMaximum()
      self.ymax = e.yMaximum()
    except:
      self.xmin = xMin()
      self.ymin = yMin()
      self.xmax = xMax()
      self.ymax = yMax()

  def xMinimum( self ):
    return self.xmin

  def yMinimum( self ):
    return self.ymin

  def xMaximum( self ):
    return self.xmax

  def yMaximum( self ):
    return self.ymax

  def width( self ):
    return self.xmax - self.xmin

  def height( self ):
    return self.ymax - self.ymin

# helper functions
def isCompatible( layer1, layer2 ):
  # check columns
  if layer1.width() != layer2.width():
    return False
  if layer1.height() != layer2.height():
    return False

  # compute cell size
  e1 = Extent( layer1 )
  w1 = e1.width() / layer1.width()
  h1 = e1.height() / layer1.height()

  e2 = Extent( layer2 )
  w2 = e2.width() / layer2.width()
  h2 = e2.height() / layer2.height()

  w = min( w1, w2 )
  h = min( h1, h2 )

  if abs( e1.xMaximum() - e2.xMaximum() ) > w:
    return False
  if abs( e1.xMinimum() - e2.xMinimum() ) > w:
    return False
  if abs( e1.yMaximum() - e2.yMaximum() ) > h:
    return False
  if abs( e1.yMinimum() - e2.yMinimum() ) > h:
    return False

  return True

def uniqueLabels( names ):
  i = 1
  labels = []

  from rastercalcengine import rasterName
  from pyparsing import LineStart, LineEnd

  validRaster = LineStart() + rasterName() + LineEnd()
  for name in names:
    name1 = "[" + name + "]"
    try:
      ss = validRaster.parseString( str( name1 ) )
    except:
      name1 = "layer"
    name1 = name1
    name2 = "[" + name
    while name1 in labels:
      name1 = name2 + "_%s]" % i
      i = i + 1
    labels.append( name1 )
  return labels

def layerAsArray( layer ):
  gdalData = gdal.Open( str( layer.source() ) )
  array = gdalData.ReadAsArray().astype( numpy.float64 )
  gdalData = None
  return array

def bandAsArray( layer, band ):
  gdalData = gdal.Open( str( layer.source() ) )
  gdalBand = gdalData.GetRasterBand(band)
  array = gdalBand.ReadAsArray().astype( numpy.float64 )
  gdalBand = None
  gdalData = None
  return array

def writeGeoTiff( arrayData, extent, pixelFormat, path, layer ):
  format = "GTiff"
  driver = gdal.GetDriverByName( format )
  metadata = driver.GetMetadata()
  if metadata.has_key( gdal.DCAP_CREATE ) and metadata[ gdal.DCAP_CREATE ] == "YES":
    pass
  else:
    print "Driver %s does not support Create() method." % format
    return False

  # get rows and columns
  dims = arrayData.shape
  if len( dims ) == 2:
    rows = dims[ 0 ]
    cols = dims[ 1 ]
    nbands = 1
  else:
    rows = dims[ 1 ]
    cols = dims[ 2 ]
    nbands = dims[ 0 ]

  pixFormat = gdal.GetDataTypeByName( pixelFormat )

  proj = projection( layer )
  trans = geotransform( layer )

  # could possible to use CreateCopy from one of the input rasters
  dst_ds = driver.Create( path, cols, rows, nbands, pixFormat )

  dst_ds.SetGeoTransform( [ extent[ 0 ], ( extent[ 2 ] - extent[ 0 ] ) / cols, 0,
                            extent[ 3 ], 0, ( extent[ 1 ] - extent[ 3 ] ) / rows ] )
  dst_ds.SetProjection( proj )

  if nbands > 1:
    for i in range( nbands ):
      dst_ds.GetRasterBand( i + 1 ).WriteArray( arrayData[ i ] )
  else:
    dst_ds.GetRasterBand( 1 ).WriteArray( arrayData )

  dst_ds = None
  return True

def outDataset( path, pixelFormat, layer, x, y ):
  format = "GTiff"
  driver = gdal.GetDriverByName( format )
  metadata = driver.GetMetadata()
  if metadata.has_key( gdal.DCAP_CREATE ) and metadata[ gdal.DCAP_CREATE ] == "YES":
    pass
  else:
    print "Driver %s does not support Create() method." % format
    return False

  pixFormat = gdal.GetDataTypeByName( pixelFormat )
  proj = projection( layer )
  trans = geotransform( layer )
  dst_ds = driver.Create( path, x, y, 1, pixFormat )
  #dst_ds.SetGeoTransform( [ extent[ 0 ], ( extent[ 2 ] - extent[ 0 ] ) / cols, 0,
  #                          extent[ 3 ], 0, ( extent[ 1 ] - extent[ 3 ] ) / rows ] )
  dst_ds.SetProjection( proj )
  dst_ds.SetGeoTransform( trans )
  return dst_ds

def projection( layer ):
  gdalData = gdal.Open( str( layer.source() ) )
  return gdalData.GetProjection()

def geotransform( layer ):
  gdalData = gdal.Open( str( layer.source() ) )
  return gdalData.GetGeoTransform()

def setRasters( rasterDict ):
  global rasterList
  rasterList = rasterDict

def getRaster( name ):
  gdalData = gdal.Open( str( rasterList[ name ].source() ) )
  array = gdalData.ReadAsArray().astype( numpy.float64 )
  gdalData = None
  return array

def getRasterBand( name, band, row, size, count ):
  gdalData = gdal.Open( str( rasterList[ name ].source() ) )
  gdalBand = gdalData.GetRasterBand(band)
  array = gdalBand.ReadAsArray( 0, row, size, count ).astype( numpy.float64 )
  gdalBand = None
  gdalData = None
  return array

def rasterSize( name ):
  gdalRaster = gdal.Open( str( rasterList[ name ].source() ) )
  x = gdalRaster.RasterXSize
  y = gdalRaster.RasterYSize
  gdalRaster = None
  return ( x, y )

def isArray( a ):
  return isNumeric( a ) or isNumpy( a )

def isNumeric( a ):
  try:
    import Numeric
    if isinstance( a, Numeric.arraytype ):
      return True
  except:
    pass
  return False

def isNumpy( a ):
  try:
    import numpy
    if isinstance( a, numpy.ndarray ):
      return True
  except:
    pass
  return False

def arrayType( a ):
  if isNumeric( a ):
    return "Numeric"
  if isNumpy( a ):
    return "Numpy"
  return None

def checkSameAs( a, b ):
  aType = arrayType( a )
  bType = arrayType( b )
  print aType, bType

  if aType == bType:
    return ( True, None )

  if bType == "Numpy":
    import numpy
    a = numpy.array( a )
    return ( False, a )

  if bType == "Numeric":
    import numeric
    a = Numeric.array( a )
    return ( False, a )

  raise ValueError, "not numpy or numeric"

# functions to work with plugin settings
def lastUsedDir():
  settings = QSettings()
  return settings.value( "/RasterCalc/lastDir", QVariant( "" ) ).toString()

def setLastUsedDir( lastDir ):
  path = QFileInfo( lastDir ).absolutePath()
  settings = QSettings()
  settings.setValue( "/RasterCalc/lastDir", QVariant( path ) )

def addToCanvas():
  settings = QSettings()
  return settings.value( "/RasterCalc/addLayer", QVariant( False ) ).toInt()[ 0 ]

def setAddToCanvas( state ):
  settings = QSettings()
  settings.setValue( "/RasterCalc/addLayer", QVariant( state ) )

