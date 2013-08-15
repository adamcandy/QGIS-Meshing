#!/usr/bin/env python

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

import os
import glob
import pytest

pwd = os.path.dirname(os.path.realpath(__file__))
root = pwd + '/../../tests/'
support = root + 'support/'
script = root + 'support_files/'


def generate_support():
  print "  Generating data files"
  os.system("python " + script + 'gaussian_bump.py ' + support + '/gaussian_bump.nc')
  os.system("grdmath " + support + "/gaussian_bump.nc 2 MUL = " + support + "/gaussian_bump_medium.nc")
  os.system("grdmath " + support + "/gaussian_bump.nc 4 MUL = " + support + "/gaussian_bump_coarse.nc")

testfiles = glob.glob(pwd + "/../../tests/*.py")

# Limit to first for now - needs investigating
testfiles = [testfiles[0]]

print 'Testing the following tests (' + str(len(testfiles)) + ' in total):'
for testfile in testfiles:
  print '  ' + os.path.basename(testfile)

pytest.main(testfiles)

#pytest.main('../../tests/')

