"""
This class includes all of the functions that used by MeshOperations.py for the creation of the mesh.
"""

from StandardModules import *
import sys
from PyQt4.QtGui import *
from export_geo import *


class PreMesh(DefineDomain):

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
		data = [self.domainData.regionIDs,self.domainData.shapes,self.boundaryIDList,self.domainData.points]
		write_geo_file(self.domainSavePath,data)
		

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
		self.postviewFileName = '%s_meshing_posfile.pos' % self.singleNetCDFLayerFileName[:-3]
		if self.dlg.ui.chooseGeoFileRadioButton.isChecked():
			self.geoFileName = self.dlg.ui.chooseGeoFileLineEdit.text()
		else:
			self.getShapeDropDownOptions()
			self.runIdDef()
			self.geoFileName = '%s.geo' % self.domainSavePath

	"""
	Generates a PostView file for the use as mesh-size metric for planar domains. The three functions for the three 
	types of coordinate system used in NetCDFs: lat-lon, x-y, and x/y start/stop with x/y step.
	"""
	def writePosFile(self):
		input_file = str(self.singleNetCDFLayerFileName)
		output_file = str(self.postviewFileName)

		# Lon-lat.
		def create_pos(netcdf_file):

			file = NetCDF.NetCDFFile(netcdf_file, 'r')
			lon = file.variables['lon'][:] 
			lat = file.variables['lat'][:]
			field = file.variables['z'][:, :] 

			pos_string = """View "background_edgelength" {\n"""
			for i in range(0,len(lon)):
				for j in range(0,len(lat)):			
					lat_p1 = lat[j]
					lon_p1 = lon[i]
					depth = abs(field[j][i])
					# If a NetCDF has 0 value elements Gmsh will attempt to create an impossibly small mesh resulting in slow
					# operation. This ensures that the .pos file created is usable.
					if depth == 0:
						depth = 0.001
					line = "SP("+str(lon_p1)+","+str(lat_p1)+",0){"+str(depth)+"};\n"
					pos_string = pos_string+line

			pos_string = pos_string+"};"
			return pos_string

		# X/Y range.
		def create_pos_xyrange(netcdf_file):

			file = NetCDF.NetCDFFile(netcdf_file, 'r')
			xMin = file.variables['x_range'][0]; xMax = file.variables['x_range'][1]
			yMin = file.variables['y_range'][0]; yMax = file.variables['y_range'][1]
			xSpace = file.variables['spacing'][0]; ySpace = file.variables['spacing'][1]
			field = file.variables['z']

			pos_string = """View "background_edgelength" {\n"""
			y = yMax; count = 0; step = 1
			xList = linspace(xMin, xMax, (1/xSpace)); yList = linspace(yMin, yMax, (1/ySpace))

			while y >= yMin:
				x = xMin
				while x <= xMax and count < len(field):
					depth = abs(field[count])
					if depth == 0:
						depth = 0.001
					line = "SP("+str(x)+","+str(y)+",0){"+str(depth)+"};\n"
					pos_string = pos_string+line
					x += step*xSpace; count += step
				y -= step*ySpace

			pos_string = pos_string+"};"
			return pos_string

		# X-Y.
		def create_pos_xy(netcdf_file):
			# read netcdf file
			file = NetCDF.NetCDFFile(netcdf_file, 'r')
			x = file.variables['x'][:] 
			y = file.variables['y'][:]
			field = file.variables['z'][:, :] 

			pos_string = """View "background_edgelength" {\n"""
			for i in range(len(x)):
				for j in range(len(y)):			
					y_p1 = y[j]
					x_p1 = x[i]
					depth = abs(field[j][i])
					if depth == 0:
						depth = 0.001
					line = "SP("+str(x_p1)+","+str(y_p1)+",0){"+str(depth)+"};\n"
					pos_string = pos_string+line

			pos_string = pos_string+"};"
			return pos_string

		print "Writing PostView File..."

		# Check the file variables so that the appropriate function can be called.
		file = NetCDF.NetCDFFile(input_file, 'r')
		variableNames = file.variables.keys()
		if 'lon' in variableNames:
			pos_string = create_pos(input_file)
		elif 'x_range' in variableNames:
			pos_string = create_pos_xyrange(input_file)
		elif 'x' in variableNames:
			pos_string = create_pos_xy(input_file)
		else:
			raise ErrorMessages.UnsuportedRasterVariableError(variableNames) #should work
		f = open(output_file,'w')
		f.write(pos_string)
		f.close()
		print "PostView File Written."

	
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



