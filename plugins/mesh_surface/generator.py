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
test = pwd+"/../../tests/output"
data = pwd+"/../../tests/support_files"

rtponedomain = data+"/rtopo_shape_DN__2.shp"
rtpmultdomain = data+"/ID0Layer.shp"

idfile = data+"/a_idLayer.shp"

ncfile = data+"/none"

print data
print rtponedomain
print rtpmultdomain
print idfile
print ncfile



print "............................................."

print "Generating data"


print "............................................."


os.system("python "+pwd+"/gaussian_bump.py "+data+"/gaussian_bump.nc")
os.system("grdmath "+data+"/gaussian_bump.nc 2 MUL = "+data+"/gaussian_bump_medium.nc")
os.system("grdmath "+data+"/gaussian_bump.nc 4 MUL = "+data+"/gaussian_bump_coarse.nc")

print "............................................."

print "Testing: annulus, Bsplines = True Compounds = False"

print "............................................."

os.system("mkdir "+test +"/annulus_BN")
os.system("python mesh_surface --line BN -g "+test+"/annulus_BN/test_annulus_BN.geo "+data+"/annulus.shp --mesh --mval 10")

print "............................................."

print "Testing: annulus, Bsplines = True Compounds = True"

print "............................................."

os.system("mkdir "+test +"/annulus_BY")
os.system("python "+pwd+"/mesh_surface --line BY -g "+test+"/annulus_BY/test_annulus_BY.geo "+data+"/annulus.shp --mesh --mval 10")
os.system("python "+pwd+"/mesh_surface --line BY -g "+test+"/annulus_BY/test_annulus_BY_metric.geo "+data+"/annulus.shp --mesh -m "+test+"/gaussian_bump.nc")
os.system("python "+pwd+"/mesh_surface --line BY -g "+test+"/annulus_BY/test_annulus_BY_medium_metric.geo "+data+"/annulus.shp --mesh -m "+test+"/gaussian_bump_medium.nc")
os.system("python "+pwd+"/mesh_surface --line BY -g "+test+"/annulus_BY/test_annulus_BY_coarse_metric.geo "+data+"/annulus.shp --mesh -m "+test+"/gaussian_bump_coarse.nc")

print "............................................."

print "Testing: annulus, Bsplines = False Compounds = True"

print "............................................."

os.system("mkdir "+test +"/annulus_LY")
os.system("python "+pwd+"/mesh_surface --line LY -g "+test+"/annulus_LY/test_annulus_LY.geo "+data+"/annulus.shp --mesh --mval 10")
os.system("python "+pwd+"/mesh_surface --line LY -g "+test+"/annulus_LY/test_annulus_LY_metric.geo "+data+"/annulus.shp --mesh -m "+test+"/gaussian_bump.nc")
os.system("python "+pwd+"/mesh_surface --line LY -g "+test+"/annulus_LY/test_annulus_LY_medium_metric.geo "+data+"/annulus.shp --mesh -m "+test+"/gaussian_bump_medium.nc")
os.system("python "+pwd+"/mesh_surface --line LY -g "+test+"/annulus_LY/test_annulus_LY_coarse_metric.geo "+data+"/annulus.shp --mesh -m "+test+"/gaussian_bump_coarse.nc")
mesh_surface


print "............................................."

print "Testing: BSplines = True Compounds = False"

print "............................................."
os.system("mkdir "+test +"/BN")
os.system("python "+pwd+"/mesh_surface --line BN -g "+test+"/BN/testfileBN_0.geo "+rtponedomain+" --mesh")
os.system("python "+pwd+"/mesh_surface --line BN -g "+test+"/BN/testfileBN_1.geo --id "+idfile+" "+rtponedomain+" --mesh")
os.system("python "+pwd+"/mesh_surface --line BN -g "+test+"/BN/testfileBN_2.geo "+rtpmultdomain+" --mesh")
os.system("python "+pwd+"/mesh_surface --line BN -g "+test+"/BN/testfileBN_3.geo --id "+idfile+" "+rtpmultdomain+"  --mesh")





print "............................................."

print "Testing: BSplines = False Compounds = True"

print "............................................."
os.system("mkdir "+test +"/LY")
os.system("python "+pwd+"/mesh_surface -l LY -g "+test+"/LY/testfileLY_0.geo "+rtponedomain+" --mesh")
os.system("python "+pwd+"/mesh_surface -l LY -g "+test+"/LY/testfileLY_1.geo --id "+idfile+" "+rtponedomain+" --mesh")
os.system("python "+pwd+"/mesh_surface -l LY -g "+test+"/LY/testfileLY_2.geo "+rtpmultdomain+" --mesh")
os.system("python "+pwd+"/mesh_surface -l LY -g "+test+"/LY/testfileLY_3.geo --id "+idfile+" "+rtpmultdomain+"  --mesh")

print "............................................."
print "Testing: BSplines = True Compounds = True"

print "............................................."

os.system("mkdir "+test +"/BY")
os.system("python "+pwd+"/mesh_surface -l BY -g "+test+"/BY/testfileBY_0."+rtponedomain+" --mesh")
os.system("python "+pwd+"/mesh_surface -l BY -g "+test+"/BY/testfileBY_1.geo --id "+idfile+" "+rtponedomain+" --mesh")
os.system("python "+pwd+"/mesh_surface -l BY -g "+test+"/BY/testfileBY_2.geo "+rtpmultdomain+" --mesh")
os.system("python "+pwd+"/mesh_surface -l BY -g "+test+"/BY/testfileBY_3.geo --id "+idfile+" "+rtpmultdomain+"  --mesh")


print '\033[1m' +  "============================================================" + '\033[0m'
print "Testing .geo files...  "




#os.system("py.test --resultlog="+pwd+"/test/test.log "+test+"/../test_geo.py")
os.system("py.test "+test+"/../test_geo.py")



print "Testing .msh files...  "

pytest.main(test+"/../test_msh.py")


print "Finished Testing"
