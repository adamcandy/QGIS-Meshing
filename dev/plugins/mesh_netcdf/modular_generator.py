#!/usr/bin/env python

import os
import glob
from modular_meshing import Modular_meshing
import pytest
#from test.test_geo import test_geo_files



pwd = os.path.dirname(os.path.realpath(__file__))
test = pwd+"/../../tests/output"
data = pwd+"/../../tests/support"



rtponedomain = data+"/rtopo_shape_DN__2.shp"
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


os.system("mkdir "+test +"/annulus_BN")

Modular_meshing("--line BN -g "+test+"/annulus_BN/test_annulus_BN.geo "+data+"/annulus.shp --mesh --mval 10")

print "............................................."

print "Testing: annulus, Bsplines = True Compounds = True"

print "............................................."

os.system("mkdir "+test +"/annulus_BY")
Modular_meshing("--line BY -g "+test+"/annulus_BY/test_annulus_BY.geo "+data+"/annulus.shp --mesh --mval 10")
Modular_meshing("--line BY -g "+test+"/annulus_BY/test_annulus_BY_metric.geo "+data+"/annulus.shp --mesh -m "+test+"/gaussian_bump.nc")
Modular_meshing("--line BY -g "+test+"/annulus_BY/test_annulus_BY_medium_metric.geo "+data+"/annulus.shp --mesh -m "+test+"/gaussian_bump_medium.nc")
Modular_meshing("--line BY -g "+test+"/annulus_BY/test_annulus_BY_coarse_metric.geo "+data+"/annulus.shp --mesh -m "+test+"/gaussian_bump_coarse.nc")

print "............................................."

print "Testing: annulus, Bsplines = False Compounds = True"

print "............................................."

os.system("mkdir "+test +"/annulus_LY")
Modular_meshing("--line LY -g "+test+"/annulus_LY/test_annulus_LY.geo "+data+"/annulus.shp --mesh --mval 10")
Modular_meshing("--line LY -g "+test+"/annulus_LY/test_annulus_LY_metric.geo "+data+"/annulus.shp --mesh -m "+test+"/gaussian_bump.nc")
Modular_meshing("--line LY -g "+test+"/annulus_LY/test_annulus_LY_medium_metric.geo "+data+"/annulus.shp --mesh -m "+test+"/gaussian_bump_medium.nc")
Modular_meshing("--line LY -g "+test+"/annulus_LY/test_annulus_LY_coarse_metric.geo "+data+"/annulus.shp --mesh -m "+test+"/gaussian_bump_coarse.nc")



print "............................................."

print "Testing: BSplines = True Compounds = False"

print "............................................."

os.system("mkdir "+test +"/BN")
Modular_meshing("--line BN -g "+test+"/BN/testfileBN_0.geo "+rtponedomain+" --mesh")
Modular_meshing("--line BN -g "+test+"/BN/testfileBN_1.geo --id "+idfile+" "+rtponedomain+" --mesh")
Modular_meshing("--line BN -g "+test+"/BN/testfileBN_2.geo "+rtpmultdomain+" --mesh")
Modular_meshing("--line BN -g "+test+"/BN/testfileBN_3.geo --id "+idfile+" "+rtpmultdomain+"  --mesh")

print "............................................."

print "Testing: BSplines = False Compounds = True"

print "............................................."


os.system("mkdir "+test +"/LY")
Modular_meshing("-l LY -g "+test+"/LY/testfileLY_0.geo "+rtponedomain+" --mesh")
Modular_meshing("-l LY -g "+test+"/LY/testfileLY_1.geo --id "+idfile+" "+rtponedomain+" --mesh")
Modular_meshing("-l LY -g "+test+"/LY/testfileLY_2.geo "+rtpmultdomain+" --mesh")
Modular_meshing("-l LY -g "+test+"/LY/testfileLY_3.geo --id "+idfile+" "+rtpmultdomain+"  --mesh")

print "............................................."
print "Testing: BSplines = True Compounds = True"

print "............................................."

os.system("mkdir "+test +"/BY")
Modular_meshing("-l BY -g "+test+"/BY/testfileBY_0."+rtponedomain+" --mesh")
Modular_meshing("-l BY -g "+test+"/BY/testfileBY_1.geo --id "+idfile+" "+rtponedomain+" --mesh")
Modular_meshing("-l BY -g "+test+"/BY/testfileBY_2.geo "+rtpmultdomain+" --mesh")
Modular_meshing("-l BY -g "+test+"/BY/testfileBY_3.geo --id "+idfile+" "+rtpmultdomain+"  --mesh")


print '\033[1m' +  "================================================================================" + '\033[0m'
print "Testing .geo files...  "

#os.system("py.test "+pwd+"/test/test_geo.py")

pytest.main(test+"/../test_geo.py")



print "Testing .msh files...  "

pytest.main(test+"/../test_msh.py")

print "Finished Testing"
