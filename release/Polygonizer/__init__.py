"""
/***************************************************************************
Polygonizer
A QGIS plugin
Creates polygons from intersecting lines
                             -------------------
begin                : 2011-01-20
copyright            : (C) 2011 by Piotr Pociask
email                : p0cisk (at) o2 pl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
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


