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

# Form implementation generated from reading ui file 'Ui_CoarsityDefiner.ui'
#
# Created: Thu Jul 12 16:45:20 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_CoarsityDefiner(object):
    def setupUi(self, CoarsityDefiner):
        CoarsityDefiner.setObjectName(_fromUtf8("CoarsityDefiner"))
        CoarsityDefiner.setEnabled(True)
        CoarsityDefiner.resize(194, 180)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        CoarsityDefiner.setFont(font)
        CoarsityDefiner.setMouseTracking(False)
        CoarsityDefiner.setAcceptDrops(False)
        CoarsityDefiner.setAutoFillBackground(False)
        CoarsityDefiner.setSizeGripEnabled(False)
        CoarsityDefiner.setModal(False)
        self.gridLayout = QtGui.QGridLayout(CoarsityDefiner)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_layer = QtGui.QLabel(CoarsityDefiner)
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.label_layer.setFont(font)
        self.label_layer.setScaledContents(False)
        self.label_layer.setWordWrap(False)
        self.label_layer.setObjectName(_fromUtf8("label_layer"))
        self.gridLayout.addWidget(self.label_layer, 0, 0, 1, 1)
        self.radioButton = QtGui.QRadioButton(CoarsityDefiner)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.gridLayout.addWidget(self.radioButton, 1, 0, 1, 1)
        self.radioButton_2 = QtGui.QRadioButton(CoarsityDefiner)
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.gridLayout.addWidget(self.radioButton_2, 2, 0, 1, 1)
        self.radioButton_3 = QtGui.QRadioButton(CoarsityDefiner)
        self.radioButton_3.setObjectName(_fromUtf8("radioButton_3"))
        self.gridLayout.addWidget(self.radioButton_3, 3, 0, 1, 1)
        self.radioButton_4 = QtGui.QRadioButton(CoarsityDefiner)
        self.radioButton_4.setEnabled(True)
        self.radioButton_4.setObjectName(_fromUtf8("radioButton_4"))
        self.gridLayout.addWidget(self.radioButton_4, 4, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(CoarsityDefiner)
        self.buttonBox.setEnabled(False)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 1)
        self.actionOpenWindow = QtGui.QAction(CoarsityDefiner)
        self.actionOpenWindow.setObjectName(_fromUtf8("actionOpenWindow"))

        self.retranslateUi(CoarsityDefiner)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CoarsityDefiner.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CoarsityDefiner.reject)
        QtCore.QObject.connect(self.radioButton, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.buttonBox.setEnabled)
        QtCore.QObject.connect(self.radioButton_2, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.buttonBox.setEnabled)
        QtCore.QObject.connect(self.radioButton_3, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.buttonBox.setEnabled)
        QtCore.QObject.connect(self.radioButton_4, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.buttonBox.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(CoarsityDefiner)

    def retranslateUi(self, CoarsityDefiner):
        CoarsityDefiner.setWindowTitle(QtGui.QApplication.translate("CoarsityDefiner", "CoarsityDefiner", None, QtGui.QApplication.UnicodeUTF8))
        self.label_layer.setText(QtGui.QApplication.translate("CoarsityDefiner", "Text label", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton.setText(QtGui.QApplication.translate("CoarsityDefiner", "One Point", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_2.setText(QtGui.QApplication.translate("CoarsityDefiner", "Two Points", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_3.setText(QtGui.QApplication.translate("CoarsityDefiner", "Three Points", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_4.setText(QtGui.QApplication.translate("CoarsityDefiner", "Four Points", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpenWindow.setText(QtGui.QApplication.translate("CoarsityDefiner", "OpenWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpenWindow.setToolTip(QtGui.QApplication.translate("CoarsityDefiner", "Opens a new window", None, QtGui.QApplication.UnicodeUTF8))

