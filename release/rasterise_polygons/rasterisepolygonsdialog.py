# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RasterisePolygonsDialog
                                 A QGIS plugin
 Rasterise polygons using their ID value and stretch canvas to the extent of background raster layer.
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
from ui_rasterisepolygons import Ui_RasterisePolygons
# create the dialog for zoom to point
class RasterisePolygonsDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_RasterisePolygons()
        self.ui.setupUi(self)
