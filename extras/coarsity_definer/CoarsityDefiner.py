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

/***************************************************************************
Name			 	 : Mesh Coarsity Definer
Description          : Helps define a mesh in terms of how finer and coarser it should be in certain points and exports it into a format which GMESH can read.
Date                 : 10/Jul/12 
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from CoarsityDefinerDialog import CoarsityDefinerDialog
#import sys

class CoarsityDefiner: 
  
  def __init__(self, iface):
    # Save reference to the QGIS interface
    self.iface = iface
    self.pinNumber = 0
    self.layer = []
    self.layerRegistry = QgsMapLayerRegistry()
    self.layerPoints = []
    self.isOn = []
    self.canvas = self.iface.mapCanvas()
    self.pinTool = QgsMapToolEmitPoint(self.canvas)
    self.provider = []

  def initGui(self):  
    # Create action that will start plugin configuration
    self.dlg = CoarsityDefinerDialog()
    self.action = QAction(QIcon(":/plugins/CoarsityDefiner/icon.png"), 
        "Define Points", self.iface.mainWindow())
    self.action.setWhatsThis("Define Points")
    
    
    self.export = QAction(QIcon(":/plugins/CoarsityDefiner/icon2.png"), 
        "Export...", self.iface.mainWindow())
    self.export.setWhatsThis("Export...")
    
    
    # connect the action to the run method
    QObject.connect(self.action, SIGNAL("activated()"), self.run) 
    QObject.connect(self.export, SIGNAL("activated()"), self.exportFile)
    QObject.connect(self.layerRegistry.instance(), SIGNAL("layerWillBeRemoved(QString)"), self.deleteLayer)

    # Add menu item
    self.iface.addPluginToMenu("&CDF", self.action)
    self.iface.addPluginToMenu("&CDF", self.export)
    result = QObject.connect(self.pinTool, SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.markMap)


  def deleteLayer(self, theLayerId):
    #When a layer is deleted
    ok = False
    ind = 0
    for c in theLayerId:
      if c >= '0' and c <='9':
        ind = ind*10 + int(c)-int('0')
        ok = True
      elif ok:
        break
    print ind
    self.isOn[ind-1] = False

  def unload(self):
    # Remove the plugin menu item and icon
    self.iface.removePluginMenu("&CDF",self.action)
    self.iface.removePluginMenu("&CDF",self.export)

  def exportFile(self):
    #get the place to write the file in
    saveFile = QFileDialog.getSaveFileName()
    if len(saveFile) == 0: #HE PRESSED CANCEL
      return
    posOutput = open(saveFile + '.pos', 'w')
    geoOutput = open(saveFile + '.geo', 'w')
    cl = 0.1
    geoOutput.write("cl = %f;\n" %cl)
    ft = QgsFeature()
    posOutput.write("View \"CDF Export\" {\n")
    n = len(self.provider)
    pointId = 0
    lineId = 0
    lineLoopId = 0
    for i in range (0, n):
      #Check it the i-th layer is still there
      if not self.isOn[i]:
        continue
      fc = self.provider[i].featureCount() #Number of points I have on this layer
      if fc==1:
        posOutput.write("SP(")
      elif fc==2:
        posOutput.write("SL(")
      elif fc==3:
        posOutput.write("ST(")
      elif fc==4:
        posOutput.write("SQ(")
      aux = pointId
      for j in range (0, fc):
       ft = QgsFeature()
       index = self.provider[i].featureAtId(j+1,ft) #Ids start from 1
       coord1 = str(ft.attributeMap()[2].toString())
       coord2 = str(ft.attributeMap()[3].toString())
       posOutput.write(coord1)
       posOutput.write(", ")
       posOutput.write(coord2)
       posOutput.write(", 0.0")
       if fc>2:
        pointId +=1
        geoOutput.write("Point(%d) = {%s, %s, 0.0, cl};\n" %(pointId, coord1, coord2))
       if j<fc-1:
        posOutput.write(", ")
      posOutput.write("){")
      aux2 = lineId
      for j in range (0, fc):
       if fc>2:
        lineId += 1
        aux += 1
        geoOutput.write("Line(%d) = {%d, %d};\n" %(lineId, aux, (aux+1) if aux<fc else (1)))
       self.provider[i].featureAtId(j+1,ft)
       coarsity = str(ft.attributeMap()[1].toString())
       posOutput.write(coarsity)
       if j<fc-1:
        posOutput.write(", ")
      if fc>2:
       lineLoopId += 1
       geoOutput.write("Line Loop(%d) = {" %lineLoopId)
       for j in range (0, fc):
        aux2 += 1
        if j < fc-1:
         geoOutput.write("%d, " %aux2)
        else:
         geoOutput.write("%d};\n" %aux2)
      geoOutput.write("Plane Surface(%d) = {%d};\n" %(lineLoopId, lineLoopId))   
     # if j<fc-1:
     #   posOutput.write(", ")
      posOutput.write("};\n")
    aux3 = ''
    for c in saveFile:
     if c == '/':
      aux3 = ''
     else:
      aux3 += c
    geoOutput.write("Merge \"%s.pos\"\n" %aux3)
    geoOutput.write("Field[1] = PostView;\nField[1].IView = 0;\nBackground Field = 1;")
    posOutput.write("};")
    geoOutput.close()
    posOutput.close()

  # run method that performs all the real work
  def run(self):
    # create and show the dialog 
    self.dlg = CoarsityDefinerDialog() 
    # show the dialog
    al = self.iface.activeLayer()
    if al:
       self.dlg.ui.label_layer.setText('Select the number of points')
    else:
       self.dlg.ui.label_layer.setText('Select a layer first')
    self.dlg.show()
    result = self.dlg.exec_()
    # See if OK was pressed
    if result == 1:
      if self.dlg.ui.radioButton.isChecked():
       numOfPoints = 1
      elif self.dlg.ui.radioButton_2.isChecked():
       numOfPoints = 2
      elif self.dlg.ui.radioButton_3.isChecked():
       numOfPoints = 3
      elif self.dlg.ui.radioButton_4.isChecked():
       numOfPoints = 4
      else:
       numOfPoints = 0
      self.newPinLayer()
      self.layerPoints.append(numOfPoints)
      self.canvas.setMapTool(self.pinTool) 

  def markMap(self, point, button):
   #If there are already enough points, just don't let the user do anything
   if self.layerPoints[self.pinNumber-1] == 0:
    return 
   ok = False
   (coarsity,_) = QInputDialog.getText(
                   self.iface.mainWindow(),
                   "Coarsity",
                   "Coaristy for the point at %.2f, %.2f" % (float(str(point.x())),float(str(point.y()))),
                   QLineEdit.Normal
                   )
   self.layerPoints[self.pinNumber-1] -= 1
   fc = int(self.provider[self.pinNumber-1].featureCount())   
   newFeature = QgsFeature()
   newFeature.setGeometry(QgsGeometry.fromPoint(point))
   newFeature.setAttributeMap( {0 : QVariant(fc),
                1 : QVariant(coarsity),
                2 : QVariant(point.x()),
                3 : QVariant(point.y())})
   self.provider[self.pinNumber-1].addFeatures([newFeature])
   self.layer[self.pinNumber-1].updateExtents()
   self.layer[self.pinNumber-1].setCacheImage(None)
   self.canvas.refresh()

  
  
  def newPinLayer(self):
   #creates a new layer for placing the pins
   self.pinNumber = self.pinNumber + 1
   layer = QgsVectorLayer("Point", "Pins - Layer %d " %self.pinNumber, "memory")
   self.provider.append(layer.dataProvider())
   self.provider[self.pinNumber-1].addAttributes([
          QgsField("id", QVariant.Int), 
          QgsField("Coarsity", QVariant.Double),
          QgsField("x", QVariant.Double),
          QgsField("y", QVariant.Double)
          ])
   layer.updateFieldMap()
   layer.setDisplayField("Coarsity")
   self.provider[self.pinNumber-1].createSpatialIndex()
   self.layerRegistry.instance().addMapLayer(layer)
   self.layer.append(layer) 
   self.isOn.append(True)
