# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MeshNetCDF
                                 A QGIS plugin
 Create Gmsh mesh from NetCDF (.nc) file where the z-coordinate is a metric for the mesh size.
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
    return "Mesh NetCDF"
def description():
    return "Create Gmsh mesh from NetCDF (.nc) file where the z-coordinate is a metric for the mesh size."
def version():
    return "Version 1.1"
def icon():
    return "icon.png"
def qgisMinimumVersion():
    return "1.0"
def classFactory(iface):
    # load MeshNetCDF class from file MeshNetCDF
    from meshnetcdf import MeshNetCDF
    return MeshNetCDF(iface)
