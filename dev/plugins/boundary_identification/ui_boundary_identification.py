# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_boundary_identification.ui'
#
# Created: Thu Jul 25 00:08:39 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_boundary_identification(object):
    def setupUi(self, boundary_identification):
        boundary_identification.setObjectName(_fromUtf8("boundary_identification"))
        boundary_identification.resize(280, 297)
        self.gridLayout = QtGui.QGridLayout(boundary_identification)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.Output_File = QtGui.QLineEdit(boundary_identification)
        self.Output_File.setObjectName(_fromUtf8("Output_File"))
        self.gridLayout.addWidget(self.Output_File, 10, 0, 1, 1)
        self.label = QtGui.QLabel(boundary_identification)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setMouseTracking(False)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.label_4 = QtGui.QLabel(boundary_identification)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 9, 0, 1, 1)
        self.label_2 = QtGui.QLabel(boundary_identification)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setMouseTracking(False)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtGui.QLabel(boundary_identification)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)
        self.Default_Id = QtGui.QLineEdit(boundary_identification)
        self.Default_Id.setObjectName(_fromUtf8("Default_Id"))
        self.gridLayout.addWidget(self.Default_Id, 7, 0, 1, 2)
        self.DomainDropdown = QtGui.QComboBox(boundary_identification)
        self.DomainDropdown.setObjectName(_fromUtf8("DomainDropdown"))
        self.gridLayout.addWidget(self.DomainDropdown, 1, 0, 1, 2)
        self.IdDropdown = QtGui.QComboBox(boundary_identification)
        self.IdDropdown.setObjectName(_fromUtf8("IdDropdown"))
        self.gridLayout.addWidget(self.IdDropdown, 3, 0, 1, 2)
        self.Browse = QtGui.QPushButton(boundary_identification)
        self.Browse.setObjectName(_fromUtf8("Browse"))
        self.gridLayout.addWidget(self.Browse, 10, 1, 1, 1)
        self.Save = QtGui.QPushButton(boundary_identification)
        self.Save.setObjectName(_fromUtf8("Save"))
        self.gridLayout.addWidget(self.Save, 12, 0, 1, 2)
        self.define_th = QtGui.QCheckBox(boundary_identification)
        self.define_th.setObjectName(_fromUtf8("define_th"))
        self.gridLayout.addWidget(self.define_th, 4, 0, 1, 1)
        self.Threshold = QtGui.QLineEdit(boundary_identification)
        self.Threshold.setEnabled(False)
        self.Threshold.setObjectName(_fromUtf8("Threshold"))
        self.gridLayout.addWidget(self.Threshold, 4, 1, 1, 1)

        self.retranslateUi(boundary_identification)
        QtCore.QObject.connect(self.Save, QtCore.SIGNAL(_fromUtf8("pressed()")), boundary_identification.accept)
        QtCore.QObject.connect(self.define_th, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.Threshold.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(boundary_identification)

    def retranslateUi(self, boundary_identification):
        boundary_identification.setWindowTitle(_translate("boundary_identification", "boundary_identification", None))
        self.label.setText(_translate("boundary_identification", "Domain", None))
        self.label_4.setText(_translate("boundary_identification", "Output File", None))
        self.label_2.setText(_translate("boundary_identification", "Id", None))
        self.label_3.setText(_translate("boundary_identification", "Default ID", None))
        self.Browse.setText(_translate("boundary_identification", "Browse", None))
        self.Save.setText(_translate("boundary_identification", "Save", None))
        self.define_th.setText(_translate("boundary_identification", "Define Threshold", None))

