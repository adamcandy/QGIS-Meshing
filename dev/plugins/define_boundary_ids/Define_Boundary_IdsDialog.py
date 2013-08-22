"""
/***************************************************************************
Name			 	 : Define Boundary Ids
Description          : Assigns boundary ids for identification in fluidity.
Date                 : 19/Jul/12 
copyright            : (C) 2012 by UROP 2012
email                : vv311@imperial.ac.uk 
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
from Ui_Define_Boundary_Ids import Ui_Define_Boundary_Ids
# create the dialog for Define_Boundary_Ids
class Define_Boundary_IdsDialog(QtGui.QDialog):
  def __init__(self): 
    QtGui.QDialog.__init__(self) 
    # Set up the user interface from Designer. 
    self.ui = Ui_Define_Boundary_Ids ()
    self.ui.setupUi(self)