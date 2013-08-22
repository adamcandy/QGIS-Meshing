"""
/***************************************************************************
Name			 	 : Define Boundary Ids
Description          : Assigns boundary ids for identification in fluidity.
Date                 : 19/Jul/12 
copyright            : (C) 2012 by UROP 2012
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
  return "Define Boundary Ids" 
def description():
  return "Assigns boundary ids for identification in fluidity."
def version(): 
  return "Version 1.1" 
def qgisMinimumVersion():
  return "1.0"
def classFactory(iface): 
  # load Define_Boundary_Ids class from file Define_Boundary_Ids
  from Define_Boundary_Ids import Define_Boundary_Ids 
  return Define_Boundary_Ids(iface)
