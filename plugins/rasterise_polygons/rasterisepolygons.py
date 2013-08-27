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

This plugin rasterises a set of polygon shapefiles and the NetCDF created will be of the same dimensions as the user-specified background NetCDF file. The implementation in QGIS for rasterisation only creates a file that is as large as the polygons bounding-box and is therefore not suitable for further raster addition, minimums etc. in other plugins.

The rasters are automatically imported into QGIS and their display changed to pseudocolour to save manual altering.
"""


# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RasterisePolygons
								 A QGIS plugin
 Rasterise polygons using their ID value and stretch canvas to the extent of background raster layer.
							  -------------------
		begin				: 2012-07-25
		copyright			: (C) 2012 by AMCG
		email				: shaun.lee10@imperial.ac.uk
 ***************************************************************************/

/***************************************************************************
 *																		 *
 *																		 *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from rasterisepolygonsdialog import RasterisePolygonsDialog

import string, re, os, argparse, sys, qgis
from numpy import *
import subprocess
from Scientific.IO import NetCDF
from PyQt4 import QtGui

class RasterisePolygons:

	def __init__(self, iface):
		# Save reference to the QGIS interface
		self.iface = iface
		# Create the dialog and keep reference
		self.dlg = RasterisePolygonsDialog()
		# initialize plugin directory
		self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/rasterisepolygons"
		# initialize locale
		localePath = ""
		locale = QSettings().value("locale/userLocale").toString()[0:2]
	   
		if QFileInfo(self.plugin_dir).exists():
			localePath = self.plugin_dir + "/i18n/rasterisepolygons_" + locale + ".qm"

		if QFileInfo(localePath).exists():
			self.translator = QTranslator()
			self.translator.load(localePath)

			if qVersion() > '4.3.3':
				QCoreApplication.installTranslator(self.translator)
   

	def initGui(self):
		# Create action that will start plugin configuration
		self.action = QAction(QIcon(":/plugins/rasterisepolygons/icon.png"), \
			u"Rasterise Polygons", self.iface.mainWindow())
		# connect the action to the run method
		QObject.connect(self.action, SIGNAL("triggered()"), self.run)
		QObject.connect(self.dlg.ui.polygonsChooseFromFilePushButton, SIGNAL("clicked()"), self.openPolygons)
		QObject.connect(self.dlg.ui.backgroundLayerChooseFromFilePushButton, SIGNAL("clicked()"), self.openBackgroundLayer)

		QObject.connect(self.dlg.ui.backgroundLayerChooseFromFileRadioButton, SIGNAL("toggled(bool)"),self.toggleBackgroundLayerChooseFromFile)
		QObject.connect(self.dlg.ui.backgroundLayerChooseFromLayerRadioButton, SIGNAL("toggled(bool)"),self.toggleBackgroundLayerChooseFromLayer)
		QObject.connect(self.dlg.ui.singlePolygonLayerRadioButton, SIGNAL("toggled(bool)"),self.toggleSinglePolygonLayer)
		QObject.connect(self.dlg.ui.polygonsChooseFromFileRadioButton, SIGNAL("toggled(bool)"),self.togglePolygonsChooseFromFile)



		

		# Add toolbar button and menu item
		self.iface.addToolBarIcon(self.action)
		self.iface.addPluginToMenu(u"&Meshing", self.action)

	"""
	Set up toggle.
	"""
	def toggleBackgroundLayerChooseFromFile(self):
		if self.dlg.ui.backgroundLayerChooseFromFileRadioButton.isChecked():
			self.dlg.ui.backgroundLayerLineEdit.setEnabled(True)
			self.dlg.ui.backgroundLayerChooseFromFilePushButton.setEnabled(True)
		else:
			self.dlg.ui.backgroundLayerLineEdit.setEnabled(False)
			self.dlg.ui.backgroundLayerChooseFromFilePushButton.setEnabled(False)

	def toggleBackgroundLayerChooseFromLayer(self):
		if self.dlg.ui.backgroundLayerChooseFromLayerRadioButton.isChecked():
			self.dlg.ui.backgroundLayerDropDown.setEnabled(True)
		else:
			self.dlg.ui.backgroundLayerDropDown.setEnabled(False)

	def toggleSinglePolygonLayer(self):
		if self.dlg.ui.singlePolygonLayerRadioButton.isChecked():
			self.dlg.ui.singlePolygonLayerDropDown.setEnabled(True)
		else:
			self.dlg.ui.singlePolygonLayerDropDown.setEnabled(False)

	def togglePolygonsChooseFromFile(self):
		if self.dlg.ui.polygonsChooseFromFileRadioButton.isChecked():
			self.dlg.ui.polygonsChooseFromFileLineEdit.setEnabled(True)
			self.dlg.ui.polygonsChooseFromFilePushButton.setEnabled(True)
		else:
			self.dlg.ui.polygonsChooseFromFileLineEdit.setEnabled(False)
			self.dlg.ui.polygonsChooseFromFilePushButton.setEnabled(False)

	"""
	Set up the browse files buttons.
	"""
	def openPolygons(self):
		self.polygonsCaption = QString("Open Polygons Shapefile")
		self.polygonsFilter = QString("Shapefiles (*.shp)")
		self.polygonsFileName = QFileDialog.getOpenFileName(caption = self.polygonsCaption, filter = self.polygonsFilter)
		self.dlg.ui.polygonsChooseFromFileLineEdit.setText(self.polygonsFileName)

	def openBackgroundLayer(self):
		self.backgroundLayerCaption = QString("Open Background Layer NetCDF")
		self.backgroundLayerFilter = QString("NetCDF Files (*.nc)")
		self.backgroundLayerChooseFileName = QFileDialog.getOpenFileName(caption = self.backgroundLayerCaption, filter = self.backgroundLayerFilter)
		self.dlg.ui.backgroundLayerLineEdit.setText(self.backgroundLayerChooseFileName)

	def getBackgroundValue(self):
		self.backgroundValue = self.dlg.ui.backgroundValueLineEdit.text()
	
	"""
	Get the active canvas layers and establish the drop-down menus.
	"""
	def getActiveLayers(self):
		self.qgisCanvas = qgis.utils.iface.mapCanvas()
		self.activeLayers = self.qgisCanvas.layers()
		return self.activeLayers

	def setDropDownOptions(self):
		self.dlg.ui.singlePolygonLayerDropDown.clear()
		self.dlg.ui.backgroundLayerDropDown.clear()

		for layer in self.activeLayers:
			if '.shp' in str(layer.source()):
				self.dlg.ui.singlePolygonLayerDropDown.addItem(layer.name(), QVariant(str(layer.source())))
	
		for layer in self.activeLayers:
			if '.nc' in str(layer.source()):
				self.dlg.ui.backgroundLayerDropDown.addItem(layer.name(), QVariant(str(layer.source())))

	"""
	Function for retrieving the user selections from the drop-downs.
	"""
	def getDropDownOptions(self):
		self.singlePolygonText = self.dlg.ui.singlePolygonLayerDropDown.currentText()
		self.singlePolygonIndex = self.dlg.ui.singlePolygonLayerDropDown.findText(self.singlePolygonText)
		self.singlePolygonFileName = self.dlg.ui.singlePolygonLayerDropDown.itemData(self.singlePolygonIndex).toString()

		self.backgroundLayerText = self.dlg.ui.backgroundLayerDropDown.currentText()
		self.backgroundLayerIndex = self.dlg.ui.backgroundLayerDropDown.findText(self.backgroundLayerText)
		self.backgroundLayerFileName = self.dlg.ui.backgroundLayerDropDown.itemData(self.backgroundLayerIndex).toString()

	"""
	Used to retrieve all of the active shapefile layers if the user selects this option.
	"""
	def getAllPolygons(self):
		self.activePolygons = []
		for layer in self.activeLayers:
			if '.shp' in str(layer.source()):
				self.activePolygons.append([layer.name(), QVariant(str(layer.source()))])

	"""
	The actual code. It is broken into three if statements depending on the user's selection. Read the first if for a detailed description, the further 	two use a similar code but with exceptions made for file source etc.
	"""
	def rasterisePolygons(self):
		# Example of system call: gdal_rasterize -a id -ts 270 220 -l boundtest-line-nodes /home/sml110/UROP/QGIS/boundtest-line-nodes.shp
		call = ["gdal_rasterize", "--version"]
		out = subprocess.Popen(call, stdout = subprocess.PIPE)
		result = out.communicate()
		result = result[0]
		result = result.split(",")
		result = result[0][5:-2]
		version = float(result)
		error = False
		if version < 1.8:
			QMessageBox.warning(None,"GDAL Error","This plugin requires gdal_rasterize version 1.8.0 or above.")
			error = True

		if error != True:
			try:
				type(eval(str(self.backgroundValue))) == int
				error = False
			except:
				QMessageBox.warning(None,"Value Error","The background value needs to be an integer.")
				error = True

			if error != True:

				# Depending on user option, open the background NetCDF.
				if self.dlg.ui.backgroundLayerChooseFromLayerRadioButton.isChecked():
					try:
						file = NetCDF.NetCDFFile(str(self.backgroundLayerFileName), 'r')
						error = False
					except:
						QMessageBox.warning(None,"Read Error","No NetCDF layer visible.")
						error = True
		
				if self.dlg.ui.backgroundLayerChooseFromFileRadioButton.isChecked():
					try:
						file = NetCDF.NetCDFFile(str(self.backgroundLayerChooseFileName), 'r')
						error = False
					except:
						QMessageBox.warning(None,"Read Error","No NetCDF file selected.")
						error = True

				if error != True:
					# Retrieve the number of columns and rows of the background mesh so the rasterised polygons layers will be of the same resolution. 
					# XY and Lon/lat NetCDF files are slightly different in their file structure hence the two options.
					try:
						# If the file is in xy space.
						if len(file.variables) == 6:
							cols = str(file.variables['dimension'][0])
							rows = str(file.variables['dimension'][1])
					
						# If the file is in lat/lon.
						if len(file.variables) == 3:
							try:
								cols = str(file.dimensions['lon'])
								rows = str(file.dimensions['lat'])

							except:
								cols = str(file.dimensions['x'])
								rows = str(file.dimensions['y'])

						error = False

					except:
						QMessageBox.warning(None,"Read Error","Could not read rows and columns of data source.")
						error = True

					if error != True:
						# Get the extent of x and y min and max so the rasterised polygons will be of the same dimensions.
						for layer in self.activeLayers:
							if str(self.backgroundLayerText) in str(layer.name()):
								extent = str(layer.extent().toString())

						minimum = extent.split(':')[0]; maximum = extent.split(':')[1]
						xMin = minimum.split(',')[0]; yMin = minimum.split(',')[1]
						xMax = maximum.split(',')[0]; yMax = maximum.split(',')[1]

						print xMin, xMax, yMin, yMax

						# Rasterise the given polygons.
						if error != True:
							if self.dlg.ui.allVisiblePolygonLayersRadioButton.isChecked():
								try:
									self.getAllPolygons()
									
									if len(list(self.activePolygons)) == 0:
										error = True
										raise ValueError ("No active polygons.")

									for i in range(len(list(self.activePolygons))):
										saveName = str(list(self.activePolygons)[i][0])
										saveFileName = str(list(self.activePolygons)[i][1].toString())
										saveFileNameTif = saveFileName.replace(".shp", ".tif")
										saveFileNameNC = saveFileName.replace(".shp", ".nc")

										# Have to rasterise to .tif and then convert to .nc as the .nc format when done directly will not import into QGIS.
										# Use initial value of 10000000 otherwise it is set to 0 and therefore when the minimum calculation is carried out in other
										# plugins it will not produce the correct results.
										subprocess.call(["gdal_rasterize", "-a", "id", "-init", str(self.backgroundValue), "-ts", cols, rows, "-te", \
										xMin, yMin, xMax, yMax, "-l", \
										saveName, str(list(self.activePolygons)[i][1].toString()), saveFileNameTif])

										# Convert into a QGIS-readable .nc.
										subprocess.call (["gdal_translate", "-of", "GMT", saveFileNameTif, saveFileNameNC])

										# Get the layer information and import into QGIS.
										fileInfo = QFileInfo(saveFileNameNC)
										baseName = fileInfo.baseName()
										self.iface.addRasterLayer(saveFileNameNC, baseName)
				
										# Refresh canvas so can change the newly added layer to pseudocolour.
										self.qgisCanvas = qgis.utils.iface.mapCanvas()
										self.activeLayers = self.qgisCanvas.layers()

										for layer in self.activeLayers:
											if saveFileNameNC in str(layer.source()):
												layer.setDrawingStyle(QgsRasterLayer.SingleBandPseudoColor)
												layer.setColorShadingAlgorithm(QgsRasterLayer.FreakOutShader)
												if hasattr(layer, "setCacheImage"): layer.setCacheImage(None)
												layer.triggerRepaint()
								except ValueError:
									QMessageBox.warning(None,"Read Error","No visible polygon layers.")
								except:
									QMessageBox.warning(None,"Error","Unable to rasterise layers. Ensure the NetCDF file is of GMT NetCDF Grid Format.")
				

							# Same operations as above but only for a single polygon.
							if self.dlg.ui.singlePolygonLayerRadioButton.isChecked():
								try:
									fileName = str(self.singlePolygonFileName)
									saveFileNameTif = fileName.replace(".shp", ".tif")
									saveFileNameNC = fileName.replace(".shp", ".nc")
									
									try:	
										subprocess.call(["gdal_rasterize", "-a", "id", "-init", str(self.backgroundValue), "-ts", cols, rows, "-te", xMin, yMin, \
									xMax, yMax, "-l", \
									str(self.singlePolygonText), str(self.singlePolygonFileName), saveFileNameTif])
										error = False
									except:
										error = True
										QMessageBox.warning(None,"Read Error","Unable to rasterise layer. Ensure the NetCDF file is of GMT NetCDF Grid Format.")
									if error != True:
											subprocess.call (["gdal_translate", "-of", "GMT", saveFileNameTif, saveFileNameNC])

											fileInfo = QFileInfo(saveFileNameNC)
											baseName = fileInfo.baseName()
											self.iface.addRasterLayer(saveFileNameNC, baseName)

											self.qgisCanvas = qgis.utils.iface.mapCanvas()
											self.activeLayers = self.qgisCanvas.layers()

											for layer in self.activeLayers:
												if saveFileNameNC in str(layer.source()):
													layer.setDrawingStyle(QgsRasterLayer.SingleBandPseudoColor)
													layer.setColorShadingAlgorithm(QgsRasterLayer.FreakOutShader)
													if hasattr(layer, "setCacheImage"): layer.setCacheImage(None)
													layer.triggerRepaint()

								except:
									QMessageBox.warning(None,"Read Error","No polygon layer selected.")

							# And again for if the user selects a .nc from file.
							if self.dlg.ui.polygonsChooseFromFileRadioButton.isChecked():
								try:
									fileName = str(self.polygonsFileName)
									if len(filename) == 0:
										error = True
										raise ValueError

									if error != True:
											saveFileNameTif = fileName.replace(".shp", ".tif")
											saveFileNameNC = fileName.replace(".shp", ".nc")

											subprocess.call(["gdal_rasterize", "-a", "id", "-init", str(self.backgroundValue), "-ts", cols, rows, "-te", xMin, \
											yMin, xMax, yMax, \
											str(self.polygonsFileName), saveFileNameTif])

											subprocess.call (["gdal_translate", "-of", "GMT", saveFileNameTif, saveFileNameNC])

											fileInfo = QFileInfo(saveFileNameNC)
											baseName = fileInfo.baseName()
											self.iface.addRasterLayer(saveFileNameNC, baseName)

											self.qgisCanvas = qgis.utils.iface.mapCanvas()
											self.activeLayers = self.qgisCanvas.layers()

											for layer in self.activeLayers:
												if saveFileNameNC in str(layer.source()):
													layer.setDrawingStyle(QgsRasterLayer.SingleBandPseudoColor)
													layer.setColorShadingAlgorithm(QgsRasterLayer.FreakOutShader)
													if hasattr(layer, "setCacheImage"): layer.setCacheImage(None)
													layer.triggerRepaint()
								except ValueError:
									QMessageBox.warning(None,"Read Error","No polygon file selected.")
								except:
									QMessageBox.warning(None,"Read Error","Unable to rasterise layer. Ensure the NetCDF file is of GMT NetCDF Grid Format.")


	def unload(self):
		# Remove the plugin menu item and icon
		self.iface.removePluginMenu(u"&Rasterise Polygons",self.action)
		self.iface.removeToolBarIcon(self.action)

	# run method that performs all the real work
	def run(self):
		# show the dialog
		self.getActiveLayers()
		self.setDropDownOptions()
		# Set the default radio buttons.
		self.dlg.ui.backgroundLayerChooseFromLayerRadioButton.setChecked(True)
		self.dlg.ui.allVisiblePolygonLayersRadioButton.setChecked(True)
		self.dlg.ui.singlePolygonLayerDropDown.setEnabled(False)
		self.dlg.ui.polygonsChooseFromFileLineEdit.setEnabled(False)
		self.dlg.ui.polygonsChooseFromFilePushButton.setEnabled(False)
		self.dlg.ui.backgroundValueLineEdit.setText(QString("10000000"))
		self.dlg.show()
		# Run the dialog event loop
		result = self.dlg.exec_()
		# See if OK was pressed
		if result == 1:
			self.getBackgroundValue()
			self.getDropDownOptions()
			self.rasterisePolygons()
