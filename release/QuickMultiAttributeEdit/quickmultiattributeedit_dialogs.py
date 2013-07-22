# --------------------------------------------------------
#    quickmultiattributeedit_dialogs - Dialog classes for quickmultiattributeedit
#
#    begin                : 19 May 2011
#    copyright            : (c) 2011 by Marco Braida
#    email                : See marcobra.ubuntu@gmail.com
#
#   QuickMultiAttributeEdit is free software and is offered 
#   without guarantee or warranty. You can redistribute it 
#   and/or modify it under the terms of version 2 of the 
#   GNU General Public License (GPL v2) as published by the 
#   Free Software Foundation (www.gnu.org).
# --------------------------------------------------------

#import os.path
import operator
import tempfile
import datetime

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from quickmultiattributeedit_library import *

from os import path, access, R_OK

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/forms")


# --------------------------------------------------------
#    quickmultiattributeedit_update_selected - Update selected feature field
# --------------------------------------------------------

from quickmultiattributeedit_update_selected_form import *

class quickmultiattributeedit_update_selected_dialog(QDialog, Ui_quickmultiattributeedit_update_selected_form):
	def __init__(self, iface):
		QDialog.__init__(self)
		self.iface = iface
		self.setupUi(self)
		#QObject.connect(self.browse, SIGNAL("clicked()"), self.browse_outfile)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.run)
		#layer = self.iface.activeLayer() # layer attivo
		layer = self.iface.mapCanvas().currentLayer()
		delimchars = "#"
		if (layer):
	                provider = layer.dataProvider()
			#provider.rewind()
			#feat = QgsFeature()
        	        #nameLayer = layer.name()
        	        # print nameLayer
			fields = provider.fields()
			if layer.type() == QgsMapLayer.VectorLayer:
				self.QLEvalore.setText("")
				self.CBfields.clear()
				#for name in fields:
				#	self.CBfields.addItem(fields[name].name())
				for (f_index, f) in fields.iteritems():
					self.CBfields.addItem(f.name(), QVariant(f_index) )
					nF = layer.selectedFeatureCount()
					if (nF > 0):		
						self.label.setText("<font color='green'>For <b>" + str(nF) +  "</b> selected elements in <b>" + layer.name() + "</b> set value of field</font>" )
						self.CBfields.setFocus(True)
						rm_if_too_old_settings_file(tempfile.gettempdir() + "/QuickMultiAttributeEdit_tmp")
						if os.path.exists( tempfile.gettempdir() + "/QuickMultiAttributeEdit_tmp"):
							in_file = open(tempfile.gettempdir() + '/QuickMultiAttributeEdit_tmp', 'r')
							file_cont = in_file.read()
							in_file.close()
							file_cont_splitted = file_cont.split(delimchars)
							lastlayer = file_cont_splitted[0]
							lastfield = file_cont_splitted[1]
							lastvalue = file_cont_splitted[2]
							lkeepLatestValue = file_cont_splitted[3]
							if ( self.CBfields.findText(lastfield) > -1 ): # se esiste il nome del campo nel combobox
								self.CBfields.setCurrentIndex(self.CBfields.findText(lastfield))
								self.cBkeepLatestValue.setChecked(str2bool(lkeepLatestValue)) # read thevalue from settings
								if ( self.cBkeepLatestValue.isChecked() ): # if true to keep latest input value
									self.QLEvalore.setText(lastvalue)
									self.QLEvalore.setFocus()

					if (nF == 0):
						infoString = QString("<font color='red'> Please select some elements into current <b>" + layer.name() + "</b> layer</font>")
						self.label.setText(infoString)
						#QMessageBox.information(self.iface.mainWindow(),"Warning",infoString)
						#self.buttonBox.setEnabled(False)
						self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
						self.QLEvalore.setEnabled(False)
						self.CBfields.setEnabled(False)
		else:
			infoString = QString("<font color='red'> <b>No layer selected... Select a layer from the layer list...</b></font>")
			#QMessageBox.information(self.iface.mainWindow(),"Warning",infoString)
			self.label.setText(infoString)
			self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
			self.QLEvalore.setEnabled(False)
			self.CBfields.setEnabled(False)

	def run(self):
	 delimchars = "#"
	 layer = self.iface.mapCanvas().currentLayer()
         if (layer == None):
		infoString = QString("<font color='red'> <b>No layer selected... Select a layer from the layer list...</b></font>")
		#QMessageBox.information(self.iface.mainWindow(),"Warning",infoString)
		self.label.setText(infoString)
	        return
         if not layer.isEditable():
		layer.startEditing()
		#infoString = QString("<font color='red'>Please activate the edit mode on the current <b>" + layer.name() + "</b> layer</font>")
		#QMessageBox.information(self.iface.mainWindow(),"Warning",infoString)
		#self.label.setText(infoString)
	    #    return

         value = unicode(self.QLEvalore.displayText())
         nPosField = self.CBfields.currentIndex()
	 #QMessageBox.information(self.iface.mainWindow(), "Update selected", str(nPosField) )
         f_index = self.CBfields.itemData( nPosField ).toInt()[0]
	 #QMessageBox.information(self.iface.mainWindow(), "Update selected", str(f_index) )
         if len(value) <= 0:
		infoString = QString("Warning <b> please input a value... </b>")
         	#QMessageBox.information(self.iface.mainWindow(), "Update selected", "Please input a value...")
		self.label.setText(infoString)
         	return
	 layer = self.iface.mapCanvas().currentLayer()
	 #layer = self.iface.activeLayer()
	 if(layer):		
	  nF = layer.selectedFeatureCount()
	  if (nF > 0):		
	   #layer.startEditing()
	   oFea = layer.selectedFeaturesIds()
	   b = QVariant(value) # value of field
	   if (nF > 1):
		#for index, field in layer.dataProvider().fields().iteritems():
		#   if str(field.name()).lower() == "campo2":
		#            nPosField = index
		#            nPosField = self.CBfields.currentIndex()
		#     	QMessageBox.information(self.iface.mainWindow(), "Update selected", str(nPosField) )
		#if nPosField <= 0:
		#   return
	    for i in oFea:
	     layer.changeAttributeValue(int(i),f_index,b) 
	   else:
	    layer.changeAttributeValue(int(oFea[0]),f_index,b) # only one feature selected
	   infoString = QString("<font color='green'> <b>You can save or abort changes at the end of sessions.<br>Press the Save icon to save or disable the edit mode of layer without save changes to abort...</b></font>")
           if not os.path.exists( tempfile.gettempdir() + "/QuickMultiAttributeEdit_tmp"):
              out_file = open(tempfile.gettempdir() + '/QuickMultiAttributeEdit_tmp', 'w')
              # out_file.write( datetime.datetime.utcnow().strftime("%s") )
		# self.CBfields.addItem(f.name(), QVariant(f_index) )
              out_file.write( layer.name() + delimchars +  unicode(self.CBfields.currentText()) + delimchars + value + delimchars + bool2str(self.cBkeepLatestValue.isChecked())  )
              out_file.close()
              QMessageBox.information(self.iface.mainWindow(),"Message",infoString)
           else:
              in_file = open(tempfile.gettempdir() + '/QuickMultiAttributeEdit_tmp', 'r')
              file_cont = in_file.read()
              in_file.close()
              file_cont_splitted = file_cont.split(delimchars)
              lastlayer = file_cont_splitted[0]
              lastfield = file_cont_splitted[1] 
              lastvalue = file_cont_splitted[2] 
              #if ( int(datetime.datetime.utcnow().strftime("%s")) - int(lastTime)  > 30 ):
              if ( lastlayer != layer.name() ):
                   QMessageBox.information(self.iface.mainWindow(),"Message",infoString)
					#else:
						#self.CBfields.setCurrentText(lastfield)
						# http://qt-project.org/doc/qt-4.8/qcombobox.html#itemData
						#QMessageBox.information(self.iface.mainWindow(),"Message",str( self.CBfields.findText(lastfield)) ) # get int idx text
						#QMessageBox.information(self.iface.mainWindow(),"Message",str( self.CBfields.currentIndex()) ) # current selected item
						#QMessageBox.information(self.iface.mainWindow(),"Message",str( self.CBfields.currentText()) ) # current selected text
						#QMessageBox.information(self.iface.mainWindow(),"Message",str( self.CBfields.itemText(3)) ) # un item alla pos 4
						#self.CBfields.setItemText(2,"pippp")
						#QMessageBox.information(self.iface.mainWindow(),"Message",str( self.CBfields[ self.CBfields.currentIndex() ] ) ) 
						#if ( self.CBfields.findText(lastfield) > -1 ): # se esiste il nome del campo nel combobox
							#self.CBfields.setCurrentIndex(self.CBfields.findText(lastfield))
							#self.CBfields.SetSelection(3)
							#self.CBfields.current(2) # seleziona detto campo
							#self.CBfields.current(lastfield)) # seleziona il campo se c'e'
              out_file = open(tempfile.gettempdir() +  '/QuickMultiAttributeEdit_tmp', 'w')
              out_file.write( layer.name() + delimchars +  unicode(self.CBfields.currentText()) + delimchars + value + delimchars + bool2str(self.cBkeepLatestValue.isChecked())  )
              # out_file.write( layer.name() )
              out_file.close()
              # if ( lastfield == 
	   #layer.commitChanges()
	  else:
	    QMessageBox.critical(self.iface.mainWindow(),"Error", "Please select at least one feature from <b> " + layer.name() + "</b> current layer")
	 else:
	  QMessageBox.critical(self.iface.mainWindow(),"Error","Please select a layer")

def bool2str(bVar):
	if bVar:
		return 'True'
	else:
		return 'False'

def str2bool(bVar):
	if ( bVar == 'True'):
		return True
	else:
		return False

def rm_if_too_old_settings_file(myPath_and_File):
	if os.path.exists(myPath_and_File) and os.path.isfile(myPath_and_File) and os.access(myPath_and_File, R_OK):
		now = time.time()
		tmpfileSectime = os.stat(myPath_and_File)[7] #get last modified time,[8] would be last creation time
		if( now - tmpfileSectime > 60 * 60 * 12 ): # if settings file is older than 6 hour
			os.remove( myPath_and_File )




