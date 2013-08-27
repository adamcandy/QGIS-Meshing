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

"""
 RasterisePolygons
"""
def name():
    return "Rasterise Polygons"

def description():
    return "Rasterise polygons using their ID value and stretch canvas to the extent of background raster layer.  Part of qgis-plugins-meshing."

def version():
    return "Version 0.3"

def icon():
    return "icon.png"

def qgisMinimumVersion():
    return "1.0"

def classFactory(iface):
    # load RasterisePolygons class from file RasterisePolygons
    from rasterisepolygons import RasterisePolygons
    return RasterisePolygons(iface)
