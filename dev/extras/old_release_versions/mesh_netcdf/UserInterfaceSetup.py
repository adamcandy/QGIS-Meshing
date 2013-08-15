from StandardModules import *

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

from PyQt4 import QtCore

'''
class to store methods which connect ui objects with functions
'''
class UsIntSetup(object):

	def __init__(self, iface):
		# Save reference to the QGIS interface
		self.iface = iface
		# Create the dialog and keep reference
		self.dlg = MeshNetCDFDialog()
		# initialize plugin directory
		self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/meshnetcdf"
		# initialize locale
		localePath = ""
		locale = QSettings().value("locale/userLocale").toString()[0:2]
	   
		if QFileInfo(self.plugin_dir).exists():
			localePath = self.plugin_dir + "/i18n/meshnetcdf_" + locale + ".qm"

		if QFileInfo(localePath).exists():
			self.translator = QTranslator()
			self.translator.load(localePath)

			if qVersion() > '4.3.3':
				QCoreApplication.installTranslator(self.translator)
	'''
	connects ui objects with functionality
	'''
	def initGui(self):
		# Create action that will start plugin configuration				
		self.action = QAction(QIcon(":/plugins/meshnetcdf/icon.png"), \
			u"Mesh NetCDF", self.iface.mainWindow())
		# connect the action to the run method
		QObject.connect(self.action, SIGNAL("triggered()"), self.run)
		QObject.connect(self.dlg.ui.singleNetCDFChooseFilesPushButton, SIGNAL("clicked()"), self.openSingleNetCDFFiles)
		QObject.connect(self.dlg.ui.chooseGeoFilePushButton, SIGNAL("clicked()"), self.openGeo)
		QtCore.QObject.connect(self.dlg.ui.multipleNetCDFFilesRadioButton, SIGNAL("toggled(bool)"),self.toggle_add_canvas)
		QtCore.QObject.connect(self.dlg.ui.singleNetCDFRadioButton, SIGNAL("toggled(bool)"),self.toggle_single_netcdf_grpbox)
		QtCore.QObject.connect(self.dlg.ui.domainShapefileLayerRadioButton, SIGNAL("toggled(bool)"),self.toggle_shapefile_drop_down)
		QtCore.QObject.connect(self.dlg.ui.chooseGeoFileRadioButton, SIGNAL("toggled(bool)"),self.toggle_choose_geo_grp)
		QtCore.QObject.connect(self.dlg.ui.define_th, SIGNAL("toggled(bool)"), self.toggle_threshold)
		QtCore.QObject.connect(self.dlg.ui.singleNetCDFChooseFilesRadioButton, SIGNAL("toggled(bool)"), self.toggle_singleNCChooseFile)

		# Add toolbar button and menu item
		self.iface.addToolBarIcon(self.action)
		self.iface.addPluginToMenu(u"&Mesh NetCDF", self.action)
		self.dlg.ui.IdDropdown.setDuplicatesEnabled(False)

		"""
		Set up enabled and disabled fields.
		"""
		self.dlg.ui.Threshold.setEnabled(False)
		self.dlg.ui.chooseGeoFileLineEdit.setEnabled(False)
		self.dlg.ui.singleNetCDFChooseFilesPushButton.setEnabled(False)
		self.dlg.ui.chooseGeoFilePushButton.setEnabled(False)

		
		"""
		Define actions for the various file browse buttons.
		"""

	'''
	obsolete method
	'''
	def toggle_threshold(self):
		if self.dlg.ui.define_th.isChecked():
			self.dlg.ui.Threshold.setEnabled(True)
		else:
			self.dlg.ui.Threshold.setEnabled(False)

	'''
	connects ui objects with functionality
	'''
	def toggle_single_netcdf_grpbox(self):
		if self.dlg.ui.singleNetCDFRadioButton.isChecked():
			self.dlg.ui.singleNetCDFGroupBox.setEnabled(True)
			self.dlg.ui.multipleNetCDFFilesRadioButton.setChecked(False)
		else:
			self.dlg.ui.singleNetCDFGroupBox.setEnabled(False)

	'''
	connects ui objects with functionality
	'''
	def toggle_shapefile_drop_down(self):
		if self.dlg.ui.domainShapefileLayerRadioButton.isChecked():
			self.dlg.ui.domainShapefileLayerDropDown.setEnabled(True)
			self.dlg.ui.grpDefID.setEnabled(True)
			self.dlg.ui.define_th.setEnabled(True)
			self.dlg.ui.chooseGeoFileRadioButton.setChecked(False)
			if self.dlg.ui.define_th.isChecked():
				self.dlg.ui.Threshold.setEnabled(True)

		else:
			self.dlg.ui.domainShapefileLayerDropDown.setEnabled(False)
			self.dlg.ui.grpDefID.setEnabled(False)
			self.dlg.ui.define_th.setEnabled(False)
			self.dlg.ui.Threshold.setEnabled(False)

	'''
	connects ui objects with functionality
	'''
	def toggle_choose_geo_grp(self):
		if self.dlg.ui.chooseGeoFileRadioButton.isChecked():
			self.dlg.ui.chooseGeoFileLineEdit.setEnabled(True)
			self.dlg.ui.chooseGeoFilePushButton.setEnabled(True)
			self.dlg.ui.domainShapefileLayerRadioButton.setChecked(False)
		else :
			self.dlg.ui.chooseGeoFileLineEdit.setEnabled(False)
			self.dlg.ui.chooseGeoFilePushButton.setEnabled(False)

	def toggle_singleNCChooseFile(self):
		if self.dlg.ui.singleNetCDFChooseFilesRadioButton.isChecked():
			self.dlg.ui.singleNetCDFChooseFilesPushButton.setEnabled(True)
		else:
			self.dlg.ui.singleNetCDFChooseFilesPushButton.setEnabled(False)

	'''
	obsolete method
	'''
	def toggle_add_canvas(self):
		if self.dlg.ui.multipleNetCDFFilesRadioButton.isChecked():
			self.dlg.ui.addLayerToCanvasCheckBox.setEnabled(True)
			self.dlg.ui.addLayerToCanvasCheckBox.setChecked(True)
			self.dlg.ui.singleNetCDFRadioButton.setChecked(False)
		else :
			self.dlg.ui.addLayerToCanvasCheckBox.setEnabled(False)
			self.dlg.ui.addLayerToCanvasCheckBox.setChecked(False)

	

	'''
	retreives the user input for the netCDF
	'''
	def openSingleNetCDFFiles(self):
		self.singleNetCDFCaption = QString("Open NetCDF")
		self.singleNetCDFFilter = QString("NetCDF Files (*.nc)")
		self.singleNetCDFFileName = QFileDialog.getOpenFileName(caption = self.singleNetCDFCaption, \
		filter = self.singleNetCDFFilter)
		self.dlg.ui.singleNetCDFChooseFilesLineEdit.setText(self.singleNetCDFFileName)
		self.netCDFToMesh = self.singleNetCDFFileName
	
	'''
	retreives the user input for the geofile
	'''
	def openGeo(self):
		self.geoCaption = QString("Open Geo File")
		self.geoFilter = QString("Geo Files (*.geo)")
		self.geoFileName = QFileDialog.getOpenFileName(caption = self.geoCaption, filter = self.geoFilter)
		self.dlg.ui.chooseGeoFileLineEdit.setText(self.geoFileName)
	
		"""
		Get the active layers and add them to the necessary drop-downs.
		"""
	'''
	imports all visible layers from qgis
	'''
	def getActiveLayers(self):
		self.qgisCanvas = qgis.utils.iface.mapCanvas()
		self.activeLayers = self.qgisCanvas.layers()

	'''
	Sets up drop down options based on active layers and sets up default id
	'''
	def setDropDownOptions(self):
		self.dlg.ui.meshingAlgorithmDropDown.clear()
		self.dlg.ui.singleNetCDFLayerDropDown.clear()
		self.dlg.ui.domainShapefileLayerDropDown.clear()

		items = list([QString("Delaunay"),QString("Frontal"),QString("MeshAdapt")])
		self.dlg.ui.meshingAlgorithmDropDown.addItems(items)

		numberOfNCs = 0
		for layer in self.activeLayers:
			if '.nc' in str(layer.source()):
				self.dlg.ui.singleNetCDFLayerDropDown.addItem(layer.name(), QVariant(str(layer.source())))
				numberOfNCs += 1
			if '.shp' in str(layer.source()):
				self.dlg.ui.domainShapefileLayerDropDown.addItem(layer.name(), QVariant(str(layer.source())))

		if numberOfNCs == 0:
			self.dlg.ui.grpNCDF.setChecked(False)
			self.dlg.ui.grpNCDF.setEnabled(False)
		else:
			self.dlg.ui.grpNCDF.setChecked(True)			
			self.dlg.ui.grpNCDF.setEnabled(True)

		self.dlg.ui.Default_Id.setText(QString('0'))

