# --------------------------------------------------------
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
