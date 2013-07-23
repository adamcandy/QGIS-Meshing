# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RasterisePolygons
                                 A QGIS plugin
 Rasterise polygons using their ID value and stretch canvas to the extent of background raster layer.
                             -------------------
        begin                : 2012-07-25
        copyright            : (C) 2012 by AMCG
        email                : shaun.lee10@imperial.ac.uk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""
def name():
    return "Rasterise Polygons"
def description():
    return "Rasterise polygons using their ID value and stretch canvas to the extent of background raster layer."
def version():
    return "Version 0.1"
def icon():
    return "icon.png"
def qgisMinimumVersion():
    return "1.0"
def classFactory(iface):
    # load RasterisePolygons class from file RasterisePolygons
    from rasterisepolygons import RasterisePolygons
    return RasterisePolygons(iface)
