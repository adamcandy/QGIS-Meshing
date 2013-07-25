import osgeo.ogr

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

shapefile = osgeo.ogr.Open("TM_WORLD_BORDERS-0.3.shp")
layer = shapefile.GetLayer(0)
countries = [] # List of (code,name,minLat,maxLat,
          # minLong,maxLong) tuples.
for i in range(layer.GetFeatureCount()):
   feature = layer.GetFeature(i)
   countryCode = feature.GetField("ISO3")
   countryName = feature.GetField("NAME")
   geometry = feature.GetGeometryRef()
   minLong,maxLong,minLat,maxLat = geometry.GetEnvelope()
   countries.append((countryName, countryCode,
      minLat, maxLat, minLong, maxLong))
   countries.sort()
for name,code,minLat,maxLat,minLong,maxLong in countries:
   print "%s (%s) lat=%0.4f..%0.4f, long=%0.4f..%0.4f" \
     % (name, code,minLat, maxLat,minLong, maxLong)
