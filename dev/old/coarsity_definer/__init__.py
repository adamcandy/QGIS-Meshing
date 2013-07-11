"""
/***************************************************************************
Name			 	 : Mesh Coarsity Definer
Description          : Helps define a mesh in terms of how finer and coarser it should be in certain points and exports it into a format which GMESH can read.
Date                 : 10/Jul/12 
copyright            : (C) 2012 by Mihai Jiplea
email                : mihai@jiplea.com 
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
  return "Mesh Coarsity Definer" 
def description():
  return "Helps define a mesh in terms of how finer and coarser it should be in certain points and exports it into a format which GMESH can read."
def version(): 
  return "Version 1.0" 
def qgisMinimumVersion():
  return "1.7.4"
def classFactory(iface): 
  # load CoarsityDefiner class from file CoarsityDefiner
  from CoarsityDefiner import CoarsityDefiner 
  return CoarsityDefiner(iface)
