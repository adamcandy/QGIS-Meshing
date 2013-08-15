# --------------------------------------------------------

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

#    __init__ - QuickMultiAttributeEdit init file
#
#    begin                : June 5, 2011
#    copyright            : (c) 2011 by Marco Braida
#    email                : See marcobra.ubuntu at gmail.com
#
#   QuickMultiAttributeEdit is free software and is offered 
#   without guarantee or warranty. You can redistribute it 
#   and/or modify it under the terms of version 2 of the 
#   GNU General Public License (GPL v2) as published by the 
#   Free Software Foundation (www.gnu.org).
# --------------------------------------------------------

from quickmultiattributeedit_menu import quickmultiattributeedit_menu

def name():
	return "QuickMultiAttributeEdit"

def description():
	return "Edit and assing same column value in the attribute table for the selected elements"

def version():
	return "1.0"

def qgisMinimumVersion():
	return "1.0"

def authorName():
	return "Marco Braida"

def icon():
    return "icons/quickmultiattributeedit_update_selected.png"
	
def classFactory(iface):
	return quickmultiattributeedit_menu(iface)
