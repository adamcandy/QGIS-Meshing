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

# Form implementation generated from reading ui file 'quickmultiattributeedit_update_selected_form.ui'
#
# Created: Tue Apr 10 11:37:31 2012
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_quickmultiattributeedit_update_selected_form(object):
    def setupUi(self, quickmultiattributeedit_update_selected_form):
        quickmultiattributeedit_update_selected_form.setObjectName("quickmultiattributeedit_update_selected_form")
        quickmultiattributeedit_update_selected_form.resize(499, 170)
        self.buttonBox = QtGui.QDialogButtonBox(quickmultiattributeedit_update_selected_form)
        self.buttonBox.setGeometry(QtCore.QRect(260, 80, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.CBfields = QtGui.QComboBox(quickmultiattributeedit_update_selected_form)
        self.CBfields.setGeometry(QtCore.QRect(10, 40, 211, 24))
        self.CBfields.setObjectName("CBfields")
        self.QLEvalore = QtGui.QLineEdit(quickmultiattributeedit_update_selected_form)
        self.QLEvalore.setGeometry(QtCore.QRect(300, 40, 161, 24))
        self.QLEvalore.setObjectName("QLEvalore")
        self.label = QtGui.QLabel(quickmultiattributeedit_update_selected_form)
        self.label.setGeometry(QtCore.QRect(10, 10, 441, 20))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(quickmultiattributeedit_update_selected_form)
        self.label_2.setGeometry(QtCore.QRect(230, 40, 61, 20))
        self.label_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(quickmultiattributeedit_update_selected_form)
        self.label_3.setGeometry(QtCore.QRect(10, 140, 471, 21))
        self.label_3.setObjectName("label_3")
        self.cBkeepLatestValue = QtGui.QCheckBox(quickmultiattributeedit_update_selected_form)
        self.cBkeepLatestValue.setGeometry(QtCore.QRect(20, 90, 211, 19))
        self.cBkeepLatestValue.setChecked(True)
        self.cBkeepLatestValue.setObjectName("cBkeepLatestValue")

        self.retranslateUi(quickmultiattributeedit_update_selected_form)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), quickmultiattributeedit_update_selected_form.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), quickmultiattributeedit_update_selected_form.reject)
        QtCore.QMetaObject.connectSlotsByName(quickmultiattributeedit_update_selected_form)

    def retranslateUi(self, quickmultiattributeedit_update_selected_form):
        quickmultiattributeedit_update_selected_form.setWindowTitle(QtGui.QApplication.translate("quickmultiattributeedit_update_selected_form", "MBupSelected", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("quickmultiattributeedit_update_selected_form", "For all selected elements in the current layer set the value of field:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("quickmultiattributeedit_update_selected_form", "equal to:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("quickmultiattributeedit_update_selected_form", "You can also activate this form with F12 funct key - by Marco Braida 2011", None, QtGui.QApplication.UnicodeUTF8))
        self.cBkeepLatestValue.setText(QtGui.QApplication.translate("quickmultiattributeedit_update_selected_form", "Keep latest input value", None, QtGui.QApplication.UnicodeUTF8))

