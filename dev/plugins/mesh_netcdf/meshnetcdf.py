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
import string, re, os, argparse, sys, os, datetime
from time import gmtime, strftime, clock
# Import the PyQt and QGIS libraries.
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import * #this is not currently working either due to qgis version or file location
import qgis             # THERE IS PROBABLY A LOT OF DUPLICATION BETWEEN THIS AND THE PREVIOUS LINE,
                        #   most likelly product of copy-paste from other plugins.

# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from meshnetcdfdialog import MeshNetCDFDialog

#from StandardModules import *
from numpy import *
from subprocess import call
from Scientific.IO import NetCDF #Most likelly obsolete this file should only deal with linking GUI to other code.

from scripts.PreMeshingFunctions import PreMesh
from scripts.MeshOperations import MeshOp
from scripts.ErrorMessages import *
from scripts.define_id import *
from scripts.flat_mesh_to_spherical import flat_mesh_spherical


class MeshNetCDF(PreMesh, MeshOp):

  def __init__(self, iface):
    # Save reference to the QGIS interface
    self.iface = iface
    # Create the dialog and keep reference
    self.dlg = MeshNetCDFDialog()
    # initialize plugin directory
    self.plugin_dir = QtCore.QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/meshnetcdf"
    # initialize locale
    localePath = ""
    locale = QtCore.QSettings().value("locale/userLocale").toString()[0:2]

    if QtCore.QFileInfo(self.plugin_dir).exists():
      localePath = self.plugin_dir + "/i18n/meshnetcdf_" + locale + ".qm"

    if QtCore.QFileInfo(localePath).exists():
      self.translator = QtCore.QTranslator()
      self.translator.load(localePath)

      if qVersion() > '4.3.3':
        QtCore.QCoreApplication.installTranslator(self.translator)

  def initGui(self):
    # Create action that will start plugin configuration                            
    self.action = QAction(QIcon(":/plugins/meshnetcdf/icon.png"), \
    u"Mesh NetCDF", self.iface.mainWindow())
    # connect the action to the run method
    QtCore.QObject.connect(self.action, SIGNAL("triggered()"), self.run)
    QtCore.QObject.connect(self.dlg.ui.singleNetCDFChooseFilesPushButton, SIGNAL("clicked()"), self.openSingleNetCDFFiles)
    QtCore.QObject.connect(self.dlg.ui.chooseGeoFilePushButton, SIGNAL("clicked()"), self.openGeo)
    QtCore.QObject.connect(self.dlg.ui.multipleNetCDFFilesRadioButton, SIGNAL("toggled(bool)"),self.toggle_add_canvas)
    QtCore.QObject.connect(self.dlg.ui.singleNetCDFRadioButton, SIGNAL("toggled(bool)"),self.toggle_single_netcdf_grpbox)
    QtCore.QObject.connect(self.dlg.ui.domainShapefileLayerRadioButton, SIGNAL("toggled(bool)"),self.toggle_shapefile_drop_down)
    QtCore.QObject.connect(self.dlg.ui.chooseGeoFileRadioButton, SIGNAL("toggled(bool)"),self.toggle_choose_geo_grp)
    QtCore.QObject.connect(self.dlg.ui.define_th, SIGNAL("toggled(bool)"), self.toggle_threshold)
    QtCore.QObject.connect(self.dlg.ui.singleNetCDFChooseFilesRadioButton, SIGNAL("toggled(bool)"), self.toggle_singleNCChooseFile)
    QtCore.QObject.connect(self.dlg.ui.commandEdit, SIGNAL("toggled(bool)"), self.toggle_commandLineEdit)

    # Add toolbar button and menu item
    self.iface.addToolBarIcon(self.action)
    self.iface.addPluginToMenu(u"&GFD Meshing", self.action)
    self.dlg.ui.IdDropdown.setDuplicatesEnabled(False)

    #Set up enabled and disabled fields.
    self.dlg.ui.Threshold.setEnabled(False)
    self.dlg.ui.chooseGeoFileLineEdit.setEnabled(False)
    self.dlg.ui.singleNetCDFChooseFilesPushButton.setEnabled(False)
    self.dlg.ui.chooseGeoFilePushButton.setEnabled(False) 

  def unload(self):
    """
    Remove the plugin menu item and icon
    """
    self.iface.removePluginMenu(u"&GFD Meshing",self.action)
    self.iface.removeToolBarIcon(self.action)

  def toggle_threshold(self):
    """
    Comment required. Apparenlty obsolete method?
    """
    if self.dlg.ui.define_th.isChecked():
      self.dlg.ui.Threshold.setEnabled(True)
    else:
      self.dlg.ui.Threshold.setEnabled(False)

  def toggle_commandLineEdit(self):
    """
    Comment required
    """
    if self.dlg.ui.commandEdit.isChecked():
      self.dlg.ui.commandTextEdit.setEnabled(True)
      self.generateMeshingOsString()
      self.dlg.ui.commandTextEdit.setText(self.mshOsString)
    else:
      self.dlg.ui.commandTextEdit.setEnabled(False)

  def toggle_single_netcdf_grpbox(self):
    """
    Comment required
    """
    if self.dlg.ui.singleNetCDFRadioButton.isChecked():
      self.dlg.ui.singleNetCDFGroupBox.setEnabled(True)
      self.dlg.ui.multipleNetCDFFilesRadioButton.setChecked(False)
    else:
      self.dlg.ui.singleNetCDFGroupBox.setEnabled(False)

  def toggle_shapefile_drop_down(self):
    """
    Comment required
    """
    if self.dlg.ui.domainShapefileLayerRadioButton.isChecked():
      self.dlg.ui.domainShapefileLayerDropDown.setEnabled(True)
      self.dlg.ui.grpDefID.setEnabled(True)
      self.dlg.ui.define_th.setEnabled(True)
      self.dlg.ui.chooseGeoFileRadioButton.setChecked(False)
      self.dlg.ui.compoundCheckBox.setEnabled(True)
      self.dlg.ui.compoundCheckBox.setChecked(True)
      self.dlg.ui.lineGroupBox.setEnabled(True)
      if self.dlg.ui.define_th.isChecked():
        self.dlg.ui.Threshold.setEnabled(True)
    else:
      self.dlg.ui.chooseGeoFileRadioButton.setChecked(True)
      self.dlg.ui.compoundCheckBox.setEnabled(False)
      self.dlg.ui.lineGroupBox.setEnabled(False)
      self.dlg.ui.compoundCheckBox.setChecked(False)
      self.dlg.ui.domainShapefileLayerDropDown.setEnabled(False)
      self.dlg.ui.grpDefID.setEnabled(False)
      self.dlg.ui.define_th.setEnabled(False)
      self.dlg.ui.Threshold.setEnabled(False)

  def toggle_choose_geo_grp(self):
    """
    Comment required
    """
    if self.dlg.ui.chooseGeoFileRadioButton.isChecked():
      self.dlg.ui.chooseGeoFileLineEdit.setEnabled(True)
      self.dlg.ui.chooseGeoFilePushButton.setEnabled(True)
      self.dlg.ui.domainShapefileLayerRadioButton.setChecked(False)
    else :
      self.dlg.ui.chooseGeoFileLineEdit.setEnabled(False)
      self.dlg.ui.domainShapefileLayerRadioButton.setChecked(True)
      self.dlg.ui.chooseGeoFilePushButton.setEnabled(False)

  def toggle_singleNCChooseFile(self):
    """
    Comment required
    """
    if self.dlg.ui.singleNetCDFChooseFilesRadioButton.isChecked():
      self.dlg.ui.singleNetCDFChooseFilesPushButton.setEnabled(True)
    else:
      self.dlg.ui.singleNetCDFChooseFilesPushButton.setEnabled(False)

  def toggle_add_canvas(self):
    """
    Comment required
    """
    if self.dlg.ui.multipleNetCDFFilesRadioButton.isChecked():
      self.dlg.ui.addLayerToCanvasCheckBox.setEnabled(True)
      self.dlg.ui.addLayerToCanvasCheckBox.setChecked(True)
      self.dlg.ui.singleNetCDFRadioButton.setChecked(False)
    else :
      self.dlg.ui.addLayerToCanvasCheckBox.setEnabled(False)
      self.dlg.ui.addLayerToCanvasCheckBox.setChecked(False)

  def openSingleNetCDFFiles(self):
    '''
    Retreives the user input for the netCDF.
    '''
    self.singleNetCDFCaption = QString("Open NetCDF")
    self.singleNetCDFFilter = QString("NetCDF Files (*.nc)")
    self.singleNetCDFFileName = QFileDialog.getOpenFileName(caption = self.singleNetCDFCaption, \
    filter = self.singleNetCDFFilter)
    self.dlg.ui.singleNetCDFChooseFilesLineEdit.setText(self.singleNetCDFFileName)
    self.netCDFToMesh = self.singleNetCDFFileName

  def openGeo(self):
    '''
    Retreives the user input for the geofile.
    '''
    self.geoCaption = QString("Open Geo File")
    self.geoFilter = QString("Geo Files (*.geo)")
    self.geoFileName = QFileDialog.getOpenFileName(caption = self.geoCaption, filter = self.geoFilter)
    self.dlg.ui.chooseGeoFileLineEdit.setText(self.geoFileName)

  def getActiveLayers(self):
    '''
    imports all visible layers from qgis
    '''
    self.qgisCanvas = qgis.utils.iface.mapCanvas()
    self.activeLayers = self.qgisCanvas.layers()

  def setDropDownOptions(self):
    '''
    Sets up drop down options based on active layers and sets up default id
    '''
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

  def getNetCDFDropDownOptions(self):
    """
    Comment required
    """
    PreMesh.getNetCDFDropDownOptions(self)

  def getShapeDropDownOptions(self):
    """
    Comment required
    """
    PreMesh.getShapeDropDownOptions(self)

  def convertShape(self):
    """
    Comment required
    """
    PreMesh.convertShape(self)

  def runIdDef(self):
    """
    Comment required
    """
    PreMesh.runIdDef(self)

  def getFiles(self):
    """
    Comment required
    """
    PreMesh.getFiles(self)

  def calculateMinimum(self):
    """
    Comment required
    """
    PreMesh.calculateMinimum(self)

  def appendGeo(self):
    """
    Comment required
    """
    MeshOp.appendGeo(self)

  def generateMesh(self):
    """
    Comment required
    """
    MeshOp.generateMesh(self)

  def functionOfBathymetry(self):
    """
    Comment required
    """
    MeshOp.functionOfBathymetry(self)

  def generateMeshingOsString(self):
    """
    Comment required
    """
    MeshOp.generateMeshingOsString(self)

  def importMsh(self):
    """
    Comment required
    """
    MeshOp.importMsh(self)

  def meshNetCDF(self):
    """
    Comment required
    """
    MeshOp.meshNetCDF(self)

# run method that performs all the real work
  def run(self):
    """
    Comment required
    """
    # show the dialog
    try :
      self.getActiveLayers()
      #if len(self.activeLayers)==0:
      #  QtGui.QMessageBox.critical(None,"Error: No Active Layer","There are no active layers. Please load a layer.")
      #  raise AssertionError ("Error: No Active Layer.")

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
        self._checkForErrors()
        self.meshNetCDF()
			
        print "Operation Stopped: " + str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
	timePassed = datetime.datetime.now() - startTime
	print "Time Elapsed: " + str(timePassed.seconds) + " seconds."

    except AssertionError as e:
      print e.message

  def _checkForErrors(self):
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
        raise AssertionError("Error: Invalid Shapefile Records")
    return False
