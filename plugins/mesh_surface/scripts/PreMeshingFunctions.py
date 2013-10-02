
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

"""
This class includes all of the functions that used by MeshOperations.py for the creation of the mesh.
"""

import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from StandardModules import *
from PyQt4.QtGui import *
from export_geo import *
import pdb
#import export_geo


class PreMesh(DefineDomain, geometry_writer):
	"""
	Once the user has selected something from the drop-downs and clicked OK these functions retrieve the layer names as well as the source files of the
	layers.
	"""

	def getNetCDFDropDownOptions(self):
		self.singleNetCDFLayerText = self.dlg.ui.singleNetCDFLayerDropDown.currentText()
		self.singleNetCDFLayerIndex = self.dlg.ui.singleNetCDFLayerDropDown.findText(self.singleNetCDFLayerText)
		self.singleNetCDFLayerFileName = self.dlg.ui.singleNetCDFLayerDropDown.itemData(self.singleNetCDFLayerIndex).toString()

	def getShapeDropDownOptions(self):
		self.domainShapefileLayerText = self.dlg.ui.domainShapefileLayerDropDown.currentText()
		self.domainShapefileLayerIndex = self.dlg.ui.domainShapefileLayerDropDown.findText(self.domainShapefileLayerText)
		self.domainShapefileLayerFileName = self.dlg.ui.domainShapefileLayerDropDown.itemData(self.domainShapefileLayerIndex).toString()

	def getMeshingAlgorithm(self):
		self.meshingAlgorithmText = self.dlg.ui.meshingAlgorithmDropDown.currentText()

	"""
	Uses getGeoFile to convert the given domain Shapefile layer into a .geo file and edits its name.
	"""
	def convertShape(self):
		getGeoFile(str(self.domainShapefileLayerFileName), str(self.domainShapefileLayerFileName[:-4]))
		self.geoFileName = '%s.geo' % self.domainShapefileLayerFileName[:-4]

	def define_bounds(self, ok):
		DefineDomain.define_bounds(self, ok)

	'''
	Runs all the modules for id definition and runs an export module to create the geofile

	Organises all the data for the id definitions and export.  exports either to sphere or
	plane.
	'''
	def runIdDef(self):
		self.defID = int(str(self.dlg.ui.Default_Id.text()))
		self.domainSavePath = '%s_idBoundary' % self.domainShapefileLayerFileName[:-4]

		self.domainText = self.domainShapefileLayerFileName[:-4]

		idText = self.dlg.ui.IdDropdown.currentText()
		idIndex = self.dlg.ui.IdDropdown.findText(idText)
		self.idFilePath = self.dlg.ui.IdDropdown.itemData(idIndex).toString()

		self.threshold = 0.0

		if self.dlg.ui.define_th.isChecked():
			self.threshold = float(str(self.dlg.ui.Threshold.text()))
		self.define_bounds(self.dlg.ui.grpDefID.isChecked())

		# Write the Geo.
		pdb.set_trace()
		geometry_writer.GeoWriter()

	"""
	Retrieve the information from the drop-down boxes.
	"""
	def getFiles(self):
		if self.dlg.ui.singleNetCDFChooseFilesRadioButton.isChecked():
			self.singleNetCDFLayerFileName = self.dlg.ui.singleNetCDFChooseFilesLineEdit.text()
			if ".nc" in str(self.singleNetCDFLayerFileName):
				self.singleNetCDFLayerFileName = '%s' % self.singleNetCDFLayerFileName
			else:
				self.singleNetCDFLayerFileName = '%s.nc' % self.singleNetCDFLayerFileName
		else:
			self.getNetCDFDropDownOptions()
		self.fieldFileName = '%s_meshing_fieldfile.fld' % self.singleNetCDFLayerFileName[:-3]
		if self.dlg.ui.chooseGeoFileRadioButton.isChecked():
			self.geoFileName = self.dlg.ui.chooseGeoFileLineEdit.text()
		else:
			self.getShapeDropDownOptions()
			self.runIdDef()
			self.geoFileName = '%s.geo' % self.domainSavePath


	"""
	Not in use. This functionality is now possible within RasterCalc.
	Performed the calculation of the minimum of multiple NetCDF files using grdmath and imported the resulting file into QGIS
	in pseudolcolour.
	"""
	def calculateMinimum(self):
		# Get all of the active NetCDF layers.
		self.activeNetCDFs = []
		for layer in self.activeLayers:
			if '.nc' in str(layer.source()):
				self.activeNetCDFs.append([layer.name(), QVariant(str(layer.source()))])

		for i in range(len(list(self.activeNetCDFs)) - 1):

			# For the first iteration we need to use the top layer and the layer below and output to /tmp/tmp.tif.
			if i == 0:
				# Min of overlapping regions.
				call (["/usr/lib/gmt/bin/grdmath", str(list(self.activeNetCDFs)[i][1].toString()), str(list(self.activeNetCDFs)[i + 1][1].toString()) \
				, "MIN", "=", "/tmp/tmp.tif"])

			# After the first iteration we want to use the newly created tmp file and the next layer down.
			if i > 0 and i < range(len(list(self.activeNetCDFs)) - 1)[-1]:
				# Min of the newly created tmp and the next layer.
				call (["/usr/lib/gmt/bin/grdmath", "/tmp/tmp.tif", str(list(self.activeNetCDFs)[i + 1][1].toString()) \
				, "MIN", "=", "/tmp/tmp.tif"])

			# For the last iteration we need to convert the .tif to a .nc with the correct filename rather than tmp.tif. Uses the bottom layers name
			# plus -minimum.nc.
			if i == range(len(list(self.activeNetCDFs)) - 1)[-1]:
				saveName = str(list(self.activeNetCDFs)[i + 1][1].toString())
				saveName = saveName.replace(".nc", "-minimum.nc")
				call (["/usr/lib/gmt/bin/grdmath", "/tmp/tmp.tif", str(list(self.activeNetCDFs)[i + 1][1].toString()) \
				, "MIN", "=", saveName])

		# If check box is selected it will add the layer to canvas as pseudocolour.
		if self.dlg.ui.addLayerToCanvasCheckBox.isChecked():
			# Add the layer and convert it to pseudocolour.
			fileInfo = QFileInfo(saveName)
			baseName = fileInfo.baseName()
			self.iface.addRasterLayer(saveName, baseName)

			self.qgisCanvas = qgis.utils.iface.mapCanvas()
			self.activeLayers = self.qgisCanvas.layers()

			for layer in self.activeLayers:
				if saveName in str(layer.source()):
					layer.setDrawingStyle(QgsRasterLayer.SingleBandPseudoColor)
					layer.setColorShadingAlgorithm(QgsRasterLayer.PseudoColorShader)



