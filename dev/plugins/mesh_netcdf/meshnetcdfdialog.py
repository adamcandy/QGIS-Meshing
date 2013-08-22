# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MeshNetCDFDialog
                                 A QGIS plugin
 Create Gmsh mesh from NetCDF (.nc) file where the z-coordinate is a metric for the mesh size.
                             -------------------
        begin                : 2012-07-25
        copyright            : (C) 2012 by AMCG
        email                : shaun.lee10@imperial.ac.uk
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
from ui_meshnetcdf import Ui_MeshNetCDF
# create the dialog for zoom to point
class MeshNetCDFDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_MeshNetCDF()
        self.ui.setupUi(self)
