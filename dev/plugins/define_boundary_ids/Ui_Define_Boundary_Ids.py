# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_Define_Boundary_Ids.ui'
#
# Created: Fri Jul 27 11:07:01 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Define_Boundary_Ids(object):
    def setupUi(self, Define_Boundary_Ids):
        Define_Boundary_Ids.setObjectName(_fromUtf8("Define_Boundary_Ids"))
        Define_Boundary_Ids.resize(280, 297)
        self.gridLayout = QtGui.QGridLayout(Define_Boundary_Ids)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.Output_File = QtGui.QLineEdit(Define_Boundary_Ids)
        self.Output_File.setObjectName(_fromUtf8("Output_File"))
        self.gridLayout.addWidget(self.Output_File, 10, 0, 1, 1)
        self.label = QtGui.QLabel(Define_Boundary_Ids)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setMouseTracking(False)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.label_4 = QtGui.QLabel(Define_Boundary_Ids)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 9, 0, 1, 1)
        self.label_2 = QtGui.QLabel(Define_Boundary_Ids)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setMouseTracking(False)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtGui.QLabel(Define_Boundary_Ids)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)
        self.Default_Id = QtGui.QLineEdit(Define_Boundary_Ids)
        self.Default_Id.setObjectName(_fromUtf8("Default_Id"))
        self.gridLayout.addWidget(self.Default_Id, 7, 0, 1, 2)
        self.DomainDropdown = QtGui.QComboBox(Define_Boundary_Ids)
        self.DomainDropdown.setObjectName(_fromUtf8("DomainDropdown"))
        self.gridLayout.addWidget(self.DomainDropdown, 1, 0, 1, 2)
        self.IdDropdown = QtGui.QComboBox(Define_Boundary_Ids)
        self.IdDropdown.setObjectName(_fromUtf8("IdDropdown"))
        self.gridLayout.addWidget(self.IdDropdown, 3, 0, 1, 2)
        self.Browse = QtGui.QPushButton(Define_Boundary_Ids)
        self.Browse.setObjectName(_fromUtf8("Browse"))
        self.gridLayout.addWidget(self.Browse, 10, 1, 1, 1)
        self.Save = QtGui.QPushButton(Define_Boundary_Ids)
        self.Save.setObjectName(_fromUtf8("Save"))
        self.gridLayout.addWidget(self.Save, 12, 0, 1, 2)
        self.define_th = QtGui.QCheckBox(Define_Boundary_Ids)
        self.define_th.setObjectName(_fromUtf8("define_th"))
        self.gridLayout.addWidget(self.define_th, 4, 0, 1, 1)
        self.Threshold = QtGui.QLineEdit(Define_Boundary_Ids)
        self.Threshold.setEnabled(False)
        self.Threshold.setObjectName(_fromUtf8("Threshold"))
        self.gridLayout.addWidget(self.Threshold, 4, 1, 1, 1)

        self.retranslateUi(Define_Boundary_Ids)
        QtCore.QObject.connect(self.Save, QtCore.SIGNAL(_fromUtf8("pressed()")), Define_Boundary_Ids.accept)
        QtCore.QObject.connect(self.define_th, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.Threshold.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Define_Boundary_Ids)

    def retranslateUi(self, Define_Boundary_Ids):
        Define_Boundary_Ids.setWindowTitle(QtGui.QApplication.translate("Define_Boundary_Ids", "Define_Boundary_Ids", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Define_Boundary_Ids", "Domain", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Define_Boundary_Ids", "Output File", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Define_Boundary_Ids", "Id", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Define_Boundary_Ids", "Default ID", None, QtGui.QApplication.UnicodeUTF8))
        self.Browse.setText(QtGui.QApplication.translate("Define_Boundary_Ids", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.Save.setText(QtGui.QApplication.translate("Define_Boundary_Ids", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.define_th.setText(QtGui.QApplication.translate("Define_Boundary_Ids", "Define Threshold", None, QtGui.QApplication.UnicodeUTF8))

