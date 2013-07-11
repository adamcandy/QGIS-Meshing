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
from PyQt4 import QtCore, QtGui 
from Ui_Meshing import Ui_Meshing
# create the dialog for Meshing
class MeshingDialog(QtGui.QDialog):
  def __init__(self): 
    QtGui.QDialog.__init__(self) 
    # Set up the user interface from Designer. 
    self.ui = Ui_Meshing ()
    self.ui.setupUi(self)