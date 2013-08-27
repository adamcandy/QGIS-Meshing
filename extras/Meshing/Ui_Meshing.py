# -*- coding: utf-8 -*-

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

# Form implementation generated from reading ui file 'Ui_Meshing.ui'
#
# Created: Fri Jul 20 14:47:08 2012
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Meshing(object):
    def setupUi(self, Meshing):
        Meshing.setObjectName("Meshing")
        Meshing.setWindowModality(QtCore.Qt.NonModal)
        Meshing.resize(509, 306)
        Meshing.setAutoFillBackground(False)
        self.geo_path = QtGui.QLineEdit(Meshing)
        self.geo_path.setGeometry(QtCore.QRect(150, 30, 241, 27))
        self.geo_path.setObjectName("geo_path")
        self.shp_path = QtGui.QLineEdit(Meshing)
        self.shp_path.setGeometry(QtCore.QRect(150, 80, 241, 27))
        self.shp_path.setObjectName("shp_path")
        self.mesh_path = QtGui.QLineEdit(Meshing)
        self.mesh_path.setGeometry(QtCore.QRect(150, 130, 241, 27))
        self.mesh_path.setObjectName("mesh_path")
        self.browse_geo = QtGui.QPushButton(Meshing)
        self.browse_geo.setGeometry(QtCore.QRect(420, 30, 71, 31))
        self.browse_geo.setObjectName("browse_geo")
        self.browse_shp = QtGui.QPushButton(Meshing)
        self.browse_shp.setGeometry(QtCore.QRect(420, 80, 71, 31))
        self.browse_shp.setObjectName("browse_shp")
        self.browse_msh = QtGui.QPushButton(Meshing)
        self.browse_msh.setGeometry(QtCore.QRect(420, 130, 71, 31))
        self.browse_msh.setObjectName("browse_msh")
        self.label = QtGui.QLabel(Meshing)
        self.label.setGeometry(QtCore.QRect(10, 40, 141, 17))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(Meshing)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 141, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(Meshing)
        self.label_3.setGeometry(QtCore.QRect(10, 130, 151, 17))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtGui.QLabel(Meshing)
        self.label_4.setGeometry(QtCore.QRect(10, 180, 141, 17))
        self.label_4.setObjectName("label_4")
        self.meshing_options = QtGui.QComboBox(Meshing)
        self.meshing_options.setGeometry(QtCore.QRect(150, 180, 241, 27))
        self.meshing_options.setObjectName("meshing_options")
        self.buttonBox = QtGui.QDialogButtonBox(Meshing)
        self.buttonBox.setGeometry(QtCore.QRect(310, 260, 176, 27))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Meshing)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Meshing.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Meshing.reject)
        QtCore.QMetaObject.connectSlotsByName(Meshing)

    def retranslateUi(self, Meshing):
        Meshing.setWindowTitle(QtGui.QApplication.translate("Meshing", "Save Files", None, QtGui.QApplication.UnicodeUTF8))
        Meshing.setAccessibleName(QtGui.QApplication.translate("Meshing", "Meshing", None, QtGui.QApplication.UnicodeUTF8))
        self.browse_geo.setText(QtGui.QApplication.translate("Meshing", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.browse_shp.setText(QtGui.QApplication.translate("Meshing", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.browse_msh.setText(QtGui.QApplication.translate("Meshing", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Meshing", "Geo File Path", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Meshing", "Shpaefile Save Path", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Meshing", "Mesh FIle Path", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Meshing", "Meshing Algorithm", None, QtGui.QApplication.UnicodeUTF8))

