"""
/***************************************************************************
Name			 	 : Mesh Coarsity Definer
Description          : Helps define a mesh in terms of how finer and coarser it should be in certain points and exports it into a format which GMESH can read.
Date                 : 10/Jul/12 
copyright            : (C) 2012 by Mihai Jiplea
email                : mihai@jiplea.com 
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
from Ui_CoarsityDefiner import Ui_CoarsityDefiner
# create the dialog for CoarsityDefiner
class CoarsityDefinerDialog(QtGui.QDialog):
  def __init__(self): 
    QtGui.QDialog.__init__(self) 
    # Set up the user interface from Designer. 
    
    self.ui = Ui_CoarsityDefiner ()
    self.ui.setupUi(self)
