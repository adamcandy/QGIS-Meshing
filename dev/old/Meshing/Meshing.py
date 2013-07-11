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
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from MeshingDialog import MeshingDialog
from subprocess import call
from makeGeoFile import *
from changeMeshToShp import getShapeForMesh
from PyQt4 import QtGui
from shutil import copyfile

class Meshing: 

	def __init__(self, iface):
		# Save reference to the QGIS interface
		self.iface = iface
		self.dlg = MeshingDialog()
		self.defaultDirec = "/tmp/qgis/"
		self.shpName = self.defaultDirec + "temp"
		self.mshName = self.defaultDirec + "temp"
		self.geoName = self.defaultDirec + "temp"
		self.meshing_option = ""
		self.meshing_option_meshAdapt = "-algo meshadapt"
		self.meshing_option_delaunay = "-algo del2d"
		self.meshing_option_frontal = "-algo front2d"

	def initGui(self):  
		# Create action that will start plugin configuration
		self.action = QAction(QIcon(":/plugins/Meshing/icon.png"), \
				"meshing", self.iface.mainWindow())
		# connect the action to the run method
		QObject.connect(self.action, SIGNAL("activated()"), self.run) 
		QObject.connect(self.dlg.ui.browse_geo, SIGNAL("clicked()"), self.save_geo)
		QObject.connect(self.dlg.ui.browse_shp, SIGNAL("clicked()"), self.save_shp)
		QObject.connect(self.dlg.ui.browse_msh, SIGNAL("clicked()"), self.save_msh)
		# Add toolbar button and menu item
		self.iface.addToolBarIcon(self.action)
		self.iface.addPluginToMenu("&meshing", self.action)
		

	#uses the file dialog to get the naem of the file from user
	def save_geo(self):
		#self.getGeoCaption = QString("Save Geo File")
		self.geoName = QFileDialog.getSaveFileName(caption=QString("Save Geo File"))
		self.dlg.ui.geo_path.setText(self.geoName)

	#uses the file dialog to get the filepath to save the shapefile for mesh
	def save_shp(self):
		#self.getShpCaption("Save Shapefile for Mesh")
		self.shpName = QFileDialog.getSaveFileName(caption=QString("Save shapefile"))
		self.dlg.ui.shp_path.setText(self.shpName)
	
	#uses the file dialog to get the filepath to save the .msh file
	def save_msh(self):
		#self.getMshCaption("Save Mesh(.msh) File")
		self.mshName = QFileDialog.getSaveFileName(caption=QString("Save Mesh File"))
		self.dlg.ui.mesh_path.setText(self.mshName)

	def unload(self):
		# Remove the plugin menu item and icon
		self.iface.removePluginMenu("&meshing",self.action)
		self.iface.removeToolBarIcon(self.action)

	#this method meshes the current active layer in qgis
	def meshCurrentLayer(self):
 		i = call(["mkdir", self.defaultDirec[0:-1]])
		if i==0: return
		try:
			aLayer = self.iface.activeLayer()
			filepath = str(aLayer.source())
		except AttributeError:
			QtGui.QMessageBox.information(None,"ERROR: No Active Layer","There are no active layer to mesh. Please load a shapefile layer first to mesh.")
			return True
		#call(["cd","~/.qgis/python/plugins/Meshing"])
		i = getGeoFile(filepath,self.geoName)
		#i = call(["python","~/.qgis/makeGeoFile_2.py",filepath,self.defaultDirec+"temp"])
		if i==2: 
			QtGui.QMessageBox.information(None,"ERROR: Creating .geo file","An error occurred while converting the current layer to a .geo file to mesh")	
			return True
		i = call(["gmsh","-2",str(self.meshing_option),self.geoName+".geo"])
		#call(["rm",self.defaultDirec+"temp.geo"])
		if i==2:
			QtGui.QMessageBox.information(None,"ERROR: In Generating Mesh","An error occurred while generating the mesh for the current layer")
			return True
		i = getShapeForMesh(self.mshName+".msh",self.shpName)
		if i==1: 
			QtGui.QMessageBox.information(None,"ERROR : Loading layer into QGIS","An eror has occured while the the meshed layer was trying to be loaded into Qgis")
			return True
		return False
	
	#this method sets up the drop down menu for user to choose the meshing
	#algorithm
	def setMeshingOption(self):
		self.dlg.ui.meshing_options.clear()
		items = list([QString("MeshAdapt"),QString("Delaunay"),QString("Frontal")])
		self.dlg.ui.meshing_options.addItems(items)

	
	"""
	This method retrieves the information from the drop down menu
	for the meshing algorithm to be used while producing the mesh
	"""
	def getMeshingOption(self):
		option = str(self.dlg.ui.meshing_options.currentText())
		if option=="MeshAdapt":
			self.meshing_option = self.meshing_option_meshAdapt
		elif option=="Delaunay":
			self.meshing_option = self.meshing_option_delaunay
		else: 
			self.meshing_option = self.meshing_option_frontal

	"""
	This method meshes the geo file hich would be produced by the current
	active layer and then displayes the shapefile of the mesh itself
	"""
	def run(self):
		QtGui.QMessageBox.information(None,"Meshing", "Please leave the file paths to save the file blank if you do not wish to save any files")
		self.setMeshingOption()
		self.dlg.show()
		result = self.dlg.exec_()
		if result==1:
			error = self.meshCurrentLayer()
			self.getMeshingOption()
			if error==True:
				return
			self.iface.addVectorLayer(self.defaultDirec+"temp.shp","Mesh","ogr")

