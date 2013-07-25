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


# Form implementation generated from reading ui file 'C:\Documents and Settings\Pocisk\.qgis\python\plugins\Polygonizer\ui_polygonizer.ui'
#
# Created: Wed Jul 27 20:12:54 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(494, 243)
        Form.setAutoFillBackground(False)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.cmbLayer = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbLayer.sizePolicy().hasHeightForWidth())
        self.cmbLayer.setSizePolicy(sizePolicy)
        self.cmbLayer.setObjectName(_fromUtf8("cmbLayer"))
        self.gridLayout.addWidget(self.cmbLayer, 1, 0, 1, 3)
        self.cbGeometry = QtGui.QCheckBox(Form)
        self.cbGeometry.setChecked(True)
        self.cbGeometry.setObjectName(_fromUtf8("cbGeometry"))
        self.gridLayout.addWidget(self.cbGeometry, 2, 0, 1, 2)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.eOutput = QtGui.QLineEdit(Form)
        self.eOutput.setObjectName(_fromUtf8("eOutput"))
        self.gridLayout.addWidget(self.eOutput, 5, 0, 1, 2)
        self.btnBrowse = QtGui.QPushButton(Form)
        self.btnBrowse.setObjectName(_fromUtf8("btnBrowse"))
        self.gridLayout.addWidget(self.btnBrowse, 5, 2, 1, 1)
        self.pbProgress = QtGui.QProgressBar(Form)
        self.pbProgress.setProperty(_fromUtf8("value"), 0)
        self.pbProgress.setObjectName(_fromUtf8("pbProgress"))
        self.gridLayout.addWidget(self.pbProgress, 6, 0, 1, 1)
        self.btnOK = QtGui.QPushButton(Form)
        self.btnOK.setObjectName(_fromUtf8("btnOK"))
        self.gridLayout.addWidget(self.btnOK, 6, 1, 1, 1)
        self.btnCancel = QtGui.QPushButton(Form)
        self.btnCancel.setFlat(False)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.gridLayout.addWidget(self.btnCancel, 6, 2, 1, 1)
        self.bAbout = QtGui.QPushButton(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bAbout.sizePolicy().hasHeightForWidth())
        self.bAbout.setSizePolicy(sizePolicy)
        self.bAbout.setMaximumSize(QtCore.QSize(25, 16777215))
        self.bAbout.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.bAbout.setFlat(True)
        self.bAbout.setObjectName(_fromUtf8("bAbout"))
        self.gridLayout.addWidget(self.bAbout, 0, 2, 1, 1)
        self.groupBox = QtGui.QGroupBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 70))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.rbNew = QtGui.QRadioButton(self.groupBox)
        self.rbNew.setChecked(True)
        self.rbNew.setObjectName(_fromUtf8("rbNew"))
        self.verticalLayout.addWidget(self.rbNew)
        self.rbOld = QtGui.QRadioButton(self.groupBox)
        self.rbOld.setObjectName(_fromUtf8("rbOld"))
        self.verticalLayout.addWidget(self.rbOld)
        self.gridLayout.addWidget(self.groupBox, 3, 0, 1, 3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.cmbLayer, self.cbGeometry)
        Form.setTabOrder(self.cbGeometry, self.rbNew)
        Form.setTabOrder(self.rbNew, self.rbOld)
        Form.setTabOrder(self.rbOld, self.eOutput)
        Form.setTabOrder(self.eOutput, self.btnBrowse)
        Form.setTabOrder(self.btnBrowse, self.btnOK)
        Form.setTabOrder(self.btnOK, self.btnCancel)
        Form.setTabOrder(self.btnCancel, self.bAbout)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Polygonizer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Input line vector layer:", None, QtGui.QApplication.UnicodeUTF8))
        self.cbGeometry.setText(QtGui.QApplication.translate("Form", "Create geometry columns", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Output file:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBrowse.setText(QtGui.QApplication.translate("Form", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOK.setText(QtGui.QApplication.translate("Form", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setText(QtGui.QApplication.translate("Form", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.bAbout.setText(QtGui.QApplication.translate("Form", "?", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Form", "Choose polygonization method", None, QtGui.QApplication.UnicodeUTF8))
        self.rbNew.setText(QtGui.QApplication.translate("Form", "New method (faster)", None, QtGui.QApplication.UnicodeUTF8))
        self.rbOld.setText(QtGui.QApplication.translate("Form", "Old method (slow, use only when new method doesn\'t work)", None, QtGui.QApplication.UnicodeUTF8))

