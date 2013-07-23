# --------------------------------------------------------
#    QuickMultiAttributeEdit_menu - QGIS plugins menu class
#
#    begin                : May 9, 2011
#    copyright            : (c) 2011 by Marco Braida
#    email                : marcobra.ubuntu at gmail.com
#
#   QuickMultiAttributeEdit is free software and is offered 
#   without guarantee or warranty. You can redistribute it 
#   and/or modify it under the terms of version 2 of the 
#   GNU General Public License (GPL v2) as published by the 
#   Free Software Foundation (www.gnu.org).
# --------------------------------------------------------

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from quickmultiattributeedit_dialogs import *

# ---------------------------------------------

class quickmultiattributeedit_menu:
	def __init__(self, iface):
		self.iface = iface

	def initGui(self):
		icon = QIcon(os.path.dirname(__file__) + "/icons/quickmultiattributeedit_update_selected.png")
		self.update_selected_action = QAction(icon, "Update field of selected features", self.iface.mainWindow())
		QObject.connect(self.update_selected_action, SIGNAL("triggered()"), self.update_selected)
		self.iface.registerMainWindowAction(self.update_selected_action, "F12") # self.update_selected_action is triggered by the F12
	       	self.iface.addToolBarIcon(self.update_selected_action)
        	self.iface.addPluginToMenu("&QuickMultiAttributeEdit", self.update_selected_action)
        	#self.iface.layerMenu().findChild(QMenu, 'menuNew').addAction(self.action)


	def unload(self):
		self.iface.unregisterMainWindowAction(self.update_selected_action)
    		self.iface.removePluginMenu("&quickmultiattributeedit", self.update_selected_action)

	def update_selected(self):
		dialog = quickmultiattributeedit_update_selected_dialog(self.iface)
		dialog.exec_()

	
