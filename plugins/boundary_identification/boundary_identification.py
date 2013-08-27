
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

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from qgis.core import *
from os import system
import pr2sph
import export_plane
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from boundary_identification_dialog import boundary_identification_dialog
# Import the algorithms for defining a boundary
from define_id import *

class boundary_identification: 

  def __init__(self, iface):
    # Save reference to the QGIS interface
    self.iface = iface
    self.dlg = boundary_identification_dialog()
    self.layerRegistry = QgsMapLayerRegistry()
    self.savePath = ""
         

  def initGui(self):  
    # Create action that will start plugin configuration
    self.action = QAction(QIcon(":/plugins/boundary_identification/icon.png"), \
        "Boundary Identification", self.iface.mainWindow())
    self.action2 = QAction(QIcon(":/plugins/boundary_identification/icon.png"), \
        "Export on Plane", self.iface.mainWindow())
    self.action3 = QAction(QIcon(":/plugins/boundary_identification/icon.png"), \
        "Export on Sphere", self.iface.mainWindow())
    # connect the action to the run method
    QObject.connect(self.action, SIGNAL("activated()"), self.run) 
    QObject.connect(self.dlg.ui.Browse, SIGNAL("clicked()"), self.browse)
    QObject.connect(self.action2, SIGNAL("activated()"), self.export)
    QObject.connect(self.action3, SIGNAL("activated()"), self.exportToSphere)
    # Add toolbar button and menu item
    self.iface.addToolBarIcon(self.action)
    self.iface.addPluginToMenu("&Meshing", self.action)
    self.iface.addPluginToMenu("&Meshing", self.action2)
    self.iface.addPluginToMenu("&Meshing", self.action3)
    self.dlg.ui.DomainDropdown.setDuplicatesEnabled(False)
    self.dlg.ui.IdDropdown.setDuplicatesEnabled(False)
   
  def unload(self):
    # Remove the plugin menu item and icon
    self.iface.removePluginMenu("&Meshing",self.action)
    self.iface.removePluginMenu("&Meshing", self.action2)
    self.iface.removePluginMenu("&Meshing", self.action3)
    self.iface.removeToolBarIcon(self.action)
  
  def browse(self):
    # Takes place when 'browse' button is activated
    filePath = QFileDialog.getSaveFileName()
    self.dlg.ui.Output_File.setText(filePath)

  def exportToSphere(self):
   try: 
    filePath = self.savePath + ".shp"
    shpFile = shapefile.Reader(str(filePath)) 
   except:
           QMessageBox.warning(None,"Read error","Shapefile not found.\nDefine ids and save the file first.")
           return
   pr2sph.export(shpFile, str(filePath) + ".geo")
   QMessageBox.information(None,"File written successfully","The .geo file has been written in the same directory as the .shp file.")

  def export(self):
   try: 
    filePath = self.savePath + ".shp"
    shpFile = shapefile.Reader(str(filePath)) 
   except:
           QMessageBox.warning(None,"Read error",".shp file not found.\nDefine ids and save the file first.")
           return
   export_plane.export(shpFile, str(filePath))
   QMessageBox.information(None,"File written successfully","The .geo file has been written in the same directory as the .shp file.")

  # run method that performs all the real work
  def run(self):
    layers = self.iface.mapCanvas().layers()
    self.dlg.ui.DomainDropdown.clear()
    self.dlg.ui.IdDropdown.clear()
    for n in layers:
      layer_n = str(n.name())
      self.dlg.ui.DomainDropdown.addItem(layer_n, QVariant(str(n.source())))
      self.dlg.ui.IdDropdown.addItem(layer_n, QVariant(str(n.source())))

    self.dlg.show()
    result = self.dlg.exec_() 
    # See if OK was pressed
    if result == 1: 
      the_id = self.dlg.ui.Default_Id.text()
      for c in the_id:
        if not (c>='0' and c<='9'):
          QMessageBox.warning(None,"Error","The id needs to be an integer.")
          return
      savePath = self.dlg.ui.Output_File.text()
      self.savePath = savePath

      #The next three lines are just a very complicated way of fetching the file path. Sometimes ui-s can be rather bad to work with.
      domainText = self.dlg.ui.DomainDropdown.currentText()
      domainIndex = self.dlg.ui.DomainDropdown.findText(domainText)
      domainFilePath = self.dlg.ui.DomainDropdown.itemData(domainIndex)

      #Fetching the other fields
      idText = self.dlg.ui.IdDropdown.currentText()
      idIndex = self.dlg.ui.IdDropdown.findText(idText)
      idFilePath = self.dlg.ui.IdDropdown.itemData(idIndex)
      threshold = 0.0
      for c in self.dlg.ui.Threshold.text():
        if not (c>='0' and c<='9'):
         QMessageBox.warning(None,"Error","The threshold needs to be a floating point number.")
         return
      if self.dlg.ui.define_th.isChecked():
       threshold = float(str(self.dlg.ui.Threshold.text()))
      print "Attempthing to generate the .shp file"
      define_bounds(str(idFilePath.toString()), str(domainFilePath.toString()), savePath, int(str(the_id)), threshold)
      try:
       self.iface.addVectorLayer(savePath+".shp","Id Layer","ogr")
      except:
       QMessageBox.warning(None,"Error","Shapefile saved but couldn't be imported into QGis.")
       return
