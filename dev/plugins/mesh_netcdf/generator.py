#!/usr/bin/env python

import os
import glob
from test.test_geo import test_geo_files

pwd = os.getcwd()
test = pwd+"/../../tests"
data = pwd+"/../../tests/data"

rtponedomain = data+"/rtopo_shape_DN_2.shp"
rtpmultdomain = data+"/ID0Layer.shp"

idfile = data+"/a_idLayer.shp"

ncfile = data+"/none"



print "............................................."

print "Generating data: Gaussian bump"


print "............................................."



os.system("python "+test+"/gaussian_bump.py "+test+"/gaussian_bump.nc")
os.system("grdmath "+test+"/gaussian_bump.nc 2 MUL = "+test+"/gaussian_bump_medium.nc")
os.system("grdmath "+test+"/gaussian_bump.nc 4 MUL = "+test+"/gaussian_bump_coarse.nc")

print "............................................."

print "Testing: annulus, Bsplines = True Compounds = False"

print "............................................."

os.system("python mesh_terminal --line BN -g "+test+"/test_annulus_BN.geo "+data+"/annulus.shp --mesh --mval 10")

print "............................................."

print "Testing: annulus, Bsplines = True Compounds = True"

print "............................................."

os.system("python mesh_terminal --line BY -g "+test+"/test_annulus_BY.geo "+data+"/annulus.shp --mesh --mval 10")
os.system("python mesh_terminal --line BY -g "+test+"/test_annulus_BY_metric.geo "+data+"/annulus.shp --mesh -m "+test+"/gaussian_bump.nc")
os.system("python mesh_terminal --line BY -g "+test+"/test_annulus_BY_medium_metric.geo "+data+"/annulus.shp --mesh -m "+test+"/gaussian_bump_medium.nc")
os.system("python mesh_terminal --line BY -g "+test+"/test_annulus_BY_coarse_metric.geo "+data+"/annulus.shp --mesh -m "+test+"/gaussian_bump_coarse.nc")

print "............................................."

print "Testing: annulus, Bsplines = False Compounds = True"

print "............................................."

os.system("python mesh_terminal --line LY -g "+test+"/test_annulus_LY.geo "+data+"/annulus.shp --mesh --mval 10")
os.system("python mesh_terminal --line LY -g "+test+"/test_annulus_LY_metric.geo "+data+"/annulus.shp --mesh -m "+test+"/gaussian_bump.nc")
os.system("python mesh_terminal --line LY -g "+test+"/test_annulus_LY_medium_metric.geo "+data+"/annulus.shp --mesh -m "+test+"/gaussian_bump_medium.nc")
os.system("python mesh_terminal --line LY -g "+test+"/test_annulus_LY_coarse_metric.geo "+data+"/annulus.shp --mesh -m "+test+"/gaussian_bump_coarse.nc")



print "............................................."

print "Testing: BSplines = True Compounds = False"

print "............................................."
os.system("python mesh_terminal --line BN -g "+test+"/testfileBN_0.geo "+rtponedomain+" --mesh")
os.system("python mesh_terminal --line BN -g "+test+"/testfileBN_1.geo --id "+idfile+" "+rtponedomain+" --mesh")
os.system("python mesh_terminal --line BN -g "+test+"/testfileBN_2.geo "+rtpmultdomain+" --mesh")
os.system("python mesh_terminal --line BN -g "+test+"/testfileBN_3.geo --id "+idfile+" "+rtpmultdomain+"  --mesh")

print "............................................."

print "Testing: BSplines = False Compounds = True"

print "............................................."
os.system("python mesh_terminal -l LY -g "+test+"/testfileLY_0.geo "+rtponedomain+" --mesh")
os.system("python mesh_terminal -l LY -g "+test+"/testfileLY_1.geo --id "+idfile+" "+rtponedomain+" --mesh")
os.system("python mesh_terminal -l LY -g "+test+"/testfileLY_2.geo "+rtpmultdomain+" --mesh")
os.system("python mesh_terminal -l LY -g "+test+"/testfileLY_3.geo --id "+idfile+" "+rtpmultdomain+"  --mesh")

print "............................................."
print "Testing: BSplines = True Compounds = True"

print "............................................."
os.system("python mesh_terminal -l BY -g "+test+"/testfileBY_0."+rtponedomain+" --mesh")
os.system("python mesh_terminal -l BY -g "+test+"/testfileBY_1.geo --id "+idfile+" "+rtponedomain+" --mesh")
os.system("python mesh_terminal -l BY -g "+test+"/testfileBY_2.geo "+rtpmultdomain+" --mesh")
os.system("python mesh_terminal -l BY -g "+test+"/testfileBY_3.geo --id "+idfile+" "+rtpmultdomain+"  --mesh")

ref = open("test/ref.geo", 'r')
test_file = open("test/test.geo", 'r')
os.system("py.test"+ test_geo_files(ref, test_file))
ref.close()
test_file.close()
  #os.system("py.test test/test_geo.py")

print  "Done Testing"







