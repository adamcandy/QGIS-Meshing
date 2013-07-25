# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_rasterisepolygons.ui'
#
# Created: Thu Jul 25 00:30:19 2013
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

class Ui_RasterisePolygons(object):
    def setupUi(self, RasterisePolygons):
        RasterisePolygons.setObjectName(_fromUtf8("RasterisePolygons"))
        RasterisePolygons.resize(532, 361)
        self.buttonBox = QtGui.QDialogButtonBox(RasterisePolygons)
        self.buttonBox.setGeometry(QtCore.QRect(170, 310, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.singlePolygonLayerDropDown = QtGui.QComboBox(RasterisePolygons)
        self.singlePolygonLayerDropDown.setEnabled(False)
        self.singlePolygonLayerDropDown.setGeometry(QtCore.QRect(240, 70, 181, 27))
        self.singlePolygonLayerDropDown.setObjectName(_fromUtf8("singlePolygonLayerDropDown"))
        self.polygonsChooseFromFileLineEdit = QtGui.QLineEdit(RasterisePolygons)
        self.polygonsChooseFromFileLineEdit.setEnabled(False)
        self.polygonsChooseFromFileLineEdit.setGeometry(QtCore.QRect(240, 100, 181, 27))
        self.polygonsChooseFromFileLineEdit.setObjectName(_fromUtf8("polygonsChooseFromFileLineEdit"))
        self.polygonsChooseFromFilePushButton = QtGui.QPushButton(RasterisePolygons)
        self.polygonsChooseFromFilePushButton.setEnabled(False)
        self.polygonsChooseFromFilePushButton.setGeometry(QtCore.QRect(430, 100, 85, 27))
        self.polygonsChooseFromFilePushButton.setObjectName(_fromUtf8("polygonsChooseFromFilePushButton"))
        self.backgroundLayerDropDown = QtGui.QComboBox(RasterisePolygons)
        self.backgroundLayerDropDown.setGeometry(QtCore.QRect(240, 180, 181, 27))
        self.backgroundLayerDropDown.setObjectName(_fromUtf8("backgroundLayerDropDown"))
        self.backgroundLayerLineEdit = QtGui.QLineEdit(RasterisePolygons)
        self.backgroundLayerLineEdit.setEnabled(False)
        self.backgroundLayerLineEdit.setGeometry(QtCore.QRect(240, 210, 181, 27))
        self.backgroundLayerLineEdit.setObjectName(_fromUtf8("backgroundLayerLineEdit"))
        self.backgroundLayerChooseFromFilePushButton = QtGui.QPushButton(RasterisePolygons)
        self.backgroundLayerChooseFromFilePushButton.setEnabled(False)
        self.backgroundLayerChooseFromFilePushButton.setGeometry(QtCore.QRect(430, 210, 85, 27))
        self.backgroundLayerChooseFromFilePushButton.setObjectName(_fromUtf8("backgroundLayerChooseFromFilePushButton"))
        self.choosePolygonsGroupBox = QtGui.QGroupBox(RasterisePolygons)
        self.choosePolygonsGroupBox.setGeometry(QtCore.QRect(10, 20, 211, 111))
        self.choosePolygonsGroupBox.setObjectName(_fromUtf8("choosePolygonsGroupBox"))
        self.layoutWidget = QtGui.QWidget(self.choosePolygonsGroupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 20, 231, 91))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.allVisiblePolygonLayersRadioButton = QtGui.QRadioButton(self.layoutWidget)
        self.allVisiblePolygonLayersRadioButton.setChecked(True)
        self.allVisiblePolygonLayersRadioButton.setObjectName(_fromUtf8("allVisiblePolygonLayersRadioButton"))
        self.verticalLayout.addWidget(self.allVisiblePolygonLayersRadioButton)
        self.singlePolygonLayerRadioButton = QtGui.QRadioButton(self.layoutWidget)
        self.singlePolygonLayerRadioButton.setObjectName(_fromUtf8("singlePolygonLayerRadioButton"))
        self.verticalLayout.addWidget(self.singlePolygonLayerRadioButton)
        self.polygonsChooseFromFileRadioButton = QtGui.QRadioButton(self.layoutWidget)
        self.polygonsChooseFromFileRadioButton.setObjectName(_fromUtf8("polygonsChooseFromFileRadioButton"))
        self.verticalLayout.addWidget(self.polygonsChooseFromFileRadioButton)
        self.chooseBackgroundGroupBox = QtGui.QGroupBox(RasterisePolygons)
        self.chooseBackgroundGroupBox.setGeometry(QtCore.QRect(10, 160, 191, 91))
        self.chooseBackgroundGroupBox.setTitle(_fromUtf8(""))
        self.chooseBackgroundGroupBox.setObjectName(_fromUtf8("chooseBackgroundGroupBox"))
        self.layoutWidget1 = QtGui.QWidget(self.chooseBackgroundGroupBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(0, 16, 181, 61))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.backgroundLayerChooseFromLayerRadioButton = QtGui.QRadioButton(self.layoutWidget1)
        self.backgroundLayerChooseFromLayerRadioButton.setChecked(True)
        self.backgroundLayerChooseFromLayerRadioButton.setObjectName(_fromUtf8("backgroundLayerChooseFromLayerRadioButton"))
        self.verticalLayout_2.addWidget(self.backgroundLayerChooseFromLayerRadioButton)
        self.backgroundLayerChooseFromFileRadioButton = QtGui.QRadioButton(self.layoutWidget1)
        self.backgroundLayerChooseFromFileRadioButton.setEnabled(True)
        self.backgroundLayerChooseFromFileRadioButton.setObjectName(_fromUtf8("backgroundLayerChooseFromFileRadioButton"))
        self.verticalLayout_2.addWidget(self.backgroundLayerChooseFromFileRadioButton)
        self.line = QtGui.QFrame(RasterisePolygons)
        self.line.setGeometry(QtCore.QRect(10, 290, 501, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label = QtGui.QLabel(RasterisePolygons)
        self.label.setGeometry(QtCore.QRect(10, 150, 399, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.backgroundValueLineEdit = QtGui.QLineEdit(RasterisePolygons)
        self.backgroundValueLineEdit.setGeometry(QtCore.QRect(240, 250, 181, 27))
        self.backgroundValueLineEdit.setObjectName(_fromUtf8("backgroundValueLineEdit"))
        self.label_2 = QtGui.QLabel(RasterisePolygons)
        self.label_2.setGeometry(QtCore.QRect(10, 260, 177, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(RasterisePolygons)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RasterisePolygons.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RasterisePolygons.reject)
        QtCore.QMetaObject.connectSlotsByName(RasterisePolygons)

    def retranslateUi(self, RasterisePolygons):
        RasterisePolygons.setWindowTitle(_translate("RasterisePolygons", "Rasterise Polygons", None))
        self.polygonsChooseFromFilePushButton.setText(_translate("RasterisePolygons", "Browse", None))
        self.backgroundLayerChooseFromFilePushButton.setText(_translate("RasterisePolygons", "Browse", None))
        self.choosePolygonsGroupBox.setTitle(_translate("RasterisePolygons", "Choose Polygons", None))
        self.allVisiblePolygonLayersRadioButton.setText(_translate("RasterisePolygons", "All Visible Polygon Layers", None))
        self.singlePolygonLayerRadioButton.setText(_translate("RasterisePolygons", "Single Polygon Layer", None))
        self.polygonsChooseFromFileRadioButton.setText(_translate("RasterisePolygons", "Choose From File", None))
        self.backgroundLayerChooseFromLayerRadioButton.setText(_translate("RasterisePolygons", "Choose From Layer", None))
        self.backgroundLayerChooseFromFileRadioButton.setText(_translate("RasterisePolygons", "Choose From File", None))
        self.label.setText(_translate("RasterisePolygons", "Choose Background Layer for the Extent of New Raster", None))
        self.label_2.setText(_translate("RasterisePolygons", "Value Outside of Polygons", None))

