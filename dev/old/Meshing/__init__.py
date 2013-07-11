"""
/***************************************************************************
Name			 	 : create a mesh
Description          : This plugin allows the user to create a mesh from a shapefile and view it in QGIS
Date                 : 11/Jul/12 
copyright            : (C) 2012 by Varun Verma
email                : vv311@imperial.ac.uk 
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
  return "create a mesh" 
def description():
  return "This plugin allows the user to create a mesh from a shapefile and view it in QGIS"
def version(): 
  return "Version 0.1" 
def qgisMinimumVersion():
  return "1.0"
def classFactory(iface): 
  # load Meshing class from file Meshing
  from Meshing import Meshing 
  return Meshing(iface)
