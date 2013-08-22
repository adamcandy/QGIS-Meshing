# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import * #this is not currently working either due to qgis version or file location
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from meshnetcdfdialog import MeshNetCDFDialog

import string, re, os, argparse, sys, os, qgis
from numpy import *
from subprocess import call
from Scientific.IO import NetCDF
from PyQt4 import QtGui

from time import gmtime, strftime, clock
import datetime
import sys

from scripts.ErrorMessages import *
from scripts.define_id import *
#import .scripts.pr2sph as pr #obs(may crash)
#import .scripts.export_plane as ep #obs
from scripts.flat_mesh_to_spherical import flat_mesh_spherical

