"""
This plugin so far calculates the minimum of of multiple NetCDF file layers using gdrmath. It needs to be extended to mesh the resulting NetCDF created or the user-sepcified file. From the UI none of the radio buttons or check boxes are functional other than those relating to Calculate Minimum as getting the min function to work took so long.
"""

# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MeshNetCDF
								 A QGIS plugin
 Create Gmsh mesh from NetCDF (.nc) file where the z-coordinate is a metric for the mesh size.
							  -------------------
		begin				: 2012-07-25
		copyright			: (C) 2012 by AMCG
		email				: shaun.lee10@imperial.ac.uk
 ***************************************************************************/

/***************************************************************************
 *																		 *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or	 *
 *   (at your option) any later version.								   *
 *																		 *
 ***************************************************************************/
"""
from StandardModules import *
import UserInterfaceSetup
import PreMeshingFunctions
import MeshOperations
import os

class MeshNetCDF(UserInterfaceSetup.UsIntSetup, PreMeshingFunctions.PreMesh, MeshOperations.MeshOp):

	def __init__(self, iface):
		UserInterfaceSetup.UsIntSetup.__init__(self, iface)
	def initGui(self):
		UserInterfaceSetup.UsIntSetup.initGui(self)
	def openSingleNetCDFFiles(self):
		UserInterfaceSetup.UsIntSetup.openSingleNetCDFFiles(self)
	def openGeo(self):
		UserInterfaceSetup.UsIntSetup.openGeo(self)
	def getActiveLayers(self):
	   	UserInterfaceSetup.UsIntSetup.getActiveLayers(self)
	def setDropDownOptions(self):
	   	UserInterfaceSetup.UsIntSetup.setDropDownOptions(self)

	def getNetCDFDropDownOptions(self):
	  	PreMeshingFunctions.PreMesh.getNetCDFDropDownOptions(self)
	def getShapeDropDownOptions(self):
		PreMeshingFunctions.PreMesh.getShapeDropDownOptions(self)
	def convertShape(self):
		PreMeshingFunctions.PreMesh.convertShape(self)
	def runIdDef(self):
		PreMeshingFunctions.PreMesh.runIdDef(self)
	def getFiles(self):
		PreMeshingFunctions.PreMesh.getFiles(self)
	def writePosFile(self):
		PreMeshingFunctions.PreMesh.writePosFile(self)
	def calculateMinimum(self):
		PreMeshingFunctions.PreMesh.calculateMinimum(self)
	
	def appendGeo(self):
		MeshOperations.MeshOp.appendGeo(self)
	def generateMesh(self):
		MeshOperations.MeshOp.generateMesh(self)
	def functionOfBathymetry(self):
		MeshOperations.MeshOp.functionOfBathymetry(self)
	def importMsh(self):
		MeshOperations.MeshOp.importMsh(self)
	def meshNetCDF(self):
		MeshOperations.MeshOp.meshNetCDF(self)

	def unload(self):
		# Remove the plugin menu item and icon
		self.iface.removePluginMenu(u"&Mesh NetCDF",self.action)
		self.iface.removeToolBarIcon(self.action)

	"""
	Using AssertionError as it is not used anywhere else in the code thereby circumventing erronous exceptions.
	"""
	def __checkForErrors(self):
		msgBox = QtGui.QMessageBox.critical
		ui = self.dlg.ui
		if ui.grpNCDF.isChecked():
			if not (ui.singleNetCDFRadioButton.isChecked() or ui.multipleNetCDFFilesRadioButton.isChecked()):
				msgBox(None,"Error: Invalid Input","Please check if given input is correct. Some radio button might not have been checked.")
				raise AssertionError ("Error: Invalid Input.")
			if ui.singleNetCDFRadioButton.isChecked():
				if not (ui.singleNetCDFLayersRadioButton.isChecked() or ui.singleNetCDFChooseFilesRadioButton.isChecked()):
					msgBox(None,"Error: Invalid Input","Please check if given input is correct. Some radio button might not have been checked.")
					raise AssertionError ("Error: Invalid Input.")

		if ui.domainShapefileLayerRadioButton.isChecked() == False and ui.chooseGeoFileRadioButton.isChecked() == False:
			msgBox(None,"Error: Invalid Input","Neither a domain Shapefile layer or Geo file was specified.")
			raise AssertionError ("Error: Invalid Input.")
				
		if ui.grpDefID.isChecked():
			def_Id = ui.Default_Id.text()
			if def_Id == "":
				msgBox(None,"Error: No Default Id specified","Please enter the Default ID.")
				raise AssertionError ("Error: No Default ID specified.")
			try :
				int(def_Id)
			except ValueError:
				msgBox(None,"Error: Invalid Default ID","Please enter a valid integer for default ID.")
				raise AssertionError ("Error: Invalid Default ID.")
			if int(def_Id) < 0 :
				msgBox(None,"Error: Invalid Default ID", "Please enter a positive number for the default ID.")
				raise AssertionError ("Error: Invalid Default ID.")
 		
		if ui.grpNCDF.isChecked() and ui.singleNetCDFRadioButton.isChecked() and ui.singleNetCDFChooseFilesRadioButton.isChecked():
			try :  
				test = open(str(ui.singleNetCDFChooseFilesLineEdit.text()),"r")
				test.close()
			except IOError:
				msgBox(None, "Error: Invalid File Path","Please enter a valid filepath for the NetCDF file.")
				raise AssertionError ("Error: Invalid File Path.")
		if ui.chooseGeoFileRadioButton.isChecked():
			try :
				test = open(str(ui.chooseGeoFileLineEdit.text()),"r")
				test.close()
			except IOError:
				msgBox(None, "Error: Invalid File Path","Please enter a valid filepath for the geo file.")
				raise AssertionError ("Error: Invalid File Path.")
		self.getShapeDropDownOptions()
		if ui.domainShapefileLayerRadioButton.isChecked():
			try:
				filepath = self.domainShapefileLayerFileName + "test"
				test = open(filepath,"w")
				test.close()
				os.remove(filepath)
			except IOError:
				msgBox(None,"Error: Permission Denied","The current domain shapefile layer is in a directory for which you do not have write permissions. Please move it to a suitable directory.")
				raise AssertionError ("Error: Permission Denied.")

			try:
				sf = shapefile.Reader(str(self.domainShapefileLayerFileName))
				sf.records()
			except ValueError:
				msgBox(None,"Error: Invalid Shapefile Records","The records for the Shapefile supplied is invalid. Ensure the polygon's ID is a positive integer.")
		return False
		

	# run method that performs all the real work
	def run(self):
		# show the dialog
		try :
			self.getActiveLayers()
			if len(self.activeLayers)==0:
				QtGui.QMessageBox.critical(None,"Error: No Active Layer","There are no active layers. Please load a layer.")
				raise AssertionError ("Error: No Active Layer.")

			self.setDropDownOptions()
			layers = self.iface.mapCanvas().layers()
			self.dlg.ui.IdDropdown.clear()
			for n in layers:
				layer_n = str(n.name())
				if ".shp" in str(n.source()):
					self.dlg.ui.IdDropdown.addItem(layer_n, QVariant(str(n.source())))
			self.dlg.show()
			self.dlg.ui.singleNetCDFLayersRadioButton.setChecked(True)
			# Run the dialog event loop
			result = self.dlg.exec_()

			# See if OK was pressed
			if result == 1:
				startTime = datetime.datetime.now()
		 		print "Operation Started: " + str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
				self.__checkForErrors()
				self.meshNetCDF()
			
				print "Operation Stopped: " + str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
				timePassed = datetime.datetime.now() - startTime
				print "Time Elapsed: " + str(timePassed.seconds) + " seconds."

		except AssertionError as e:
			print e.message


