
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
This class performs the meshing of the geo file generated in PreMeshingFunctions.py. It allows the use of NetCDF 
files as a mesh-size metric on a planar surface or the generation of a mesh with no NetCDF specified. Once the 
geo file has been appropriately appended to include the necessary field it meshes the file with the selected 
meshing algorithm in the background and opens the .msh in Gmsh.
"""

#from mesh_surface.StandardModules import * #check that this hasn't broken it
import subprocess
from PosFileConverter import *
from PyQt4 import QtCore, QtGui
from scripts.bathy_to_field import create_fld_file

class MeshOp( converter ):

	"""
	Merge the PostView file created by writePosFile in PreMeshingFunctions.py. The PostView file is a set of Scalar 
	Points and therefore needs to be triangulated. As each point is a mesh-size metric it can be used as the background 
	field.
	"""

	def gradeToNCFlat_OLD(self):

		f = open(str(self.geoFileName), 'a')

		f.write('\n//Code added by Mesh Surface to merge the created PostView file and use it as mesh-size metric.\n')
		f.write('Merge "%s";\n' % str(self.postviewFileName))
		f.write('Field[1] = PostView;\n')
		f.write('Field[1].IView = 1;\n')
		f.write('Plugin(Triangulate).Run;\n')
		f.write('Background Field = 1;\n')
		f.write('Mesh.CharacteristicLengthExtendFromBoundary = 0;\n')
                f.write('Mesh.CharacteristicLengthFromPoints = 0;\n')
		f.close()

	def gradeToNCFlat(self):

		f = open(str(self.geoFileName), 'a')
                f.write('\nField[1] = Structured;\n')
                f.write('Field[1].FileName = "%s";\n' % self.fieldFileName)
                f.write('Field[1].TextFormat = 1;\n')
                f.write("Background Field = 1;\n")
                f.close()
	

	"""
	Currently not working. The code here doesn't produce any errors but the method it implements is incorrect. 
	Once complete it should perform similarily to gradeToNCFlat as it uses a NetCDF file as a mesh-size metric.
	"""
	def gradeToNCSphere(self):
		
		self.meshFile = flat_mesh_spherical(self.meshFile,self.dlg.ui.steriographicRadioButton.isChecked())

	"""
	This function is used if no NetCDF file has been specified. It sets up an Attractor and Threshold background field 
	so the mesh produced is finer around the coastline and coarser away from the coast.
	"""
	def noNetCDFMesh(self):
		geoFile = open(str(self.geoFileName), 'a')
		geoFile.write('\n//Code added by Mesh Surface to create uniform mesh.\n')#need to add in code to convert to steriographic, is there a possition field in GMSH?, yes! x,y,z are the spartial coordinates and can be used in math eval, though probably unesicary given that constant mesh is projected
		geoFile.write("Field[1] = MathEval;\n")
		geoFile.write('Field[1].F = "10000";\n')
		geoFile.write("Background Field = 1;\n")
		geoFile.close()


	def generateMeshingOsString(self):
		meshingAlgorithmText = str(self.dlg.ui.meshingAlgorithmDropDown.currentText())

		if meshingAlgorithmText == 'Delaunay':
			meshingAlgorithmText = 'del2d'

		elif meshingAlgorithmText == 'Frontal':
			meshingAlgorithmText = 'front2d'

		elif meshingAlgorithmText == 'MeshAdapt':
			meshingAlgorithmText = 'meshadapt'
		try:
			self.mshOsString = 'gmsh -2 ' + '-algo ' + meshingAlgorithmText + ' ' + "\""+str(self.geoFileName)+"\" "
		except:#not the best way of coding this; change
			domainShapefileLayerTextTemp = self.dlg.ui.domainShapefileLayerDropDown.currentText()
			domainShapefileLayerIndexTemp = self.dlg.ui.domainShapefileLayerDropDown.findText(domainShapefileLayerTextTemp)
			domainShapefileLayerFileNameTemp = self.dlg.ui.domainShapefileLayerDropDown.itemData(domainShapefileLayerIndexTemp).toString()
			geoFileNameTemp = '%s.geo' % domainShapefileLayerFileNameTemp[:-4]
			self.mshOsString = 'gmsh -2 ' + '-algo ' + meshingAlgorithmText + ' ' + "\""+str(geoFileNameTemp)+"\" "

	"""
	Retrieves the meshing algorithm specified in the drop down box, meshes the geo file that has been appended with the 
	fields from one of the functions above and opens this mesh in Gmsh. 
	The geo file is meshed using the given algorithm through a system call "gmsh -2 - algo algorithm geoFile".
	"""
	def generateMesh(self):
	
		print 'Generating Mesh...'
		
		if self.dlg.ui.commandEdit.isChecked():
			self.mshOsString = str(self.dlg.ui.commandTextEdit.toPlainText())#this may give poor results
		else:
			self.generateMeshingOsString()
		
		print "System Call: " + self.mshOsString
		print "Gmsh Output:"
		print "--------------------------"
		os.system(str(self.mshOsString))
		self.meshFile = '%s.msh' % self.geoFileName[:-4]

		# There were a couple of times when the script would fail but still create an empty .msh that was opened, hence these catches.
		try:
			file = open(self.meshFile, "r")
		except IOError:
			raise AssertionError ("Error: No Msh file created.")
		
		call  = ["tail", "--lines=1", str(self.meshFile)]
		out = subprocess.Popen(call, stdout = subprocess.PIPE)
		result = out.communicate()

		if "$EndElements" not in result[0]:
			msgBox = QtGui.QMessageBox.critical
			msgBox(None,"Error: Incomplete Mesh File","The meshing was either interrupted or there is not enough available disk space.")
			raise AssertionError ("Error: Incomplete Mesh file.")

		print "--------------------------"
		print 'Mesh Generated.'

		# If the Spherical button is selected use this function to project it onto the sphere.
		if self.dlg.ui.sphereRadioButton.isChecked() or self.dlg.ui.steriographicRadioButton.isChecked():#change
			print "Projecting to Sphere..."
			self.gradeToNCSphere()
			print "Mesh Projected."

		osString = 'gmsh ' + "\"" + str(self.meshFile) + "\" &"
		print osString
		os.system(str(osString))

		print '\nFiles Created:'
		print 'Geo: ' + str(self.geoFileName) 
		print 'Mesh: ' + str(self.meshFile)
		if self.dlg.ui.grpNCDF.isChecked():
			print "PostView: " + str(self.postviewFileName)

	def openGeoFile(self):
		osString = 'gmsh ' + "\"" + str(self.geoFileName) + "\" &"
		print osString
		os.system(str(osString))

		print '\nFiles Created:'
		print 'Geo: ' + str(self.geoFileName)

	def filesCreated(self):
		if self.dlg.ui.grpCSpace_2.isChecked():
			fileString = "Geo File: " + str(self.geoFileName) + "\nMsh File: %s" % str(self.meshFile)

		else:
			fileString = "Geo File: " + str(self.geoFileName)

		QtGui.QMessageBox.information(None, "Files Created", fileString)


	"""
	Currently not called. It converts the generated mesh into a Shapefile to be viewed in QGIS. However, each triangle of the 
	mesh is represented as an individual polygon so anything other than an ideal, simple meshes are unfeasibly large to 
	manipulate in QGIS causing it to freeze.
	"""
	def importMsh(self):
		msh = self.dlg.ui.geoFileLineEdit.text()
		msh.replace(".geo", ".msh")
		i = getShapeForMesh(msh, "/tmp/temp")
		if i==1: 
			QMessageBox.information(None,"Error: Loading layer into QGIS","An error has occured while the the meshed layer was trying to be loaded into Qgis %s" %msh)
			return
		self.iface.addVectorLayer("/tmp/temp.shp","Mesh","ogr")


	def writePosFileOLD( self ):
		converter.writePosFile(self)

	def writePosFile( self ):
		create_fld_file(self.singleNetCDFLayerFileName,self.fieldFileName)
	
	"""
	Calls all of the functions required to produce the mesh.
	"""
	def MeshSurface(self):
		self.getFiles()	

		if self.dlg.ui.grpNCDF.isChecked():

			if (self.dlg.ui.multipleNetCDFFilesRadioButton.isChecked()): self.calculateMinimum()

			self.writePosFile()
			self.gradeToNCFlat()

		else:
			self.noNetCDFMesh()

		if self.dlg.ui.grpCSpace_2.isChecked():
			self.generateMesh()

		else:
			self.openGeoFile()

		self.filesCreated()
