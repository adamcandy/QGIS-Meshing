"""

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

/***************************************************************************
Polygonizer
A QGIS plugin
Creates polygons from intersecting lines
                             -------------------
begin                : 2011-01-20
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *                                                                         *
 ***************************************************************************/
Changelog:
2.0
-new calculation method - using shapely union (much, much faster)
-summary of calculation (time and number of created polygons)
-new icon ;)

1.0
-improved calculation speed (about 15% faster)
-first non-experimental release

0.3
-fix error -> only visible lines were polygonized if whole layer wasn't displayed in map window
-temp layers aren't visible

0.2
-add progress bar
-add geometry columns creation (area and perimeter)

0.1
-first release
****************************************************************************/

 This script initializes the plugin, making it known to QGIS.
"""
def name():
  return "Polygonizer"
def description():
  return "Creates polygons from intersecting lines (requires shapely library)"
def version():
  return "Version 2.0"
def icon():
  return "icon.png"
def qgisMinimumVersion():
  return "1.5"
def authorName():
  return "Piotr Pociask"
def classFactory(iface):
  # load Polygonizer class from file Polygonizer
  from polygonizer import Polygonizer
  return Polygonizer(iface)


