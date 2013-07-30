import os
import glob
import pytest

pwd = os.path.dirname(os.path.realpath(__file__))
test = pwd+"/../../tests/output"
data = pwd+"/../../tests/support"

print "\n......................................................."

print ".           Generating data: Gaussian bump            ."

print ".......................................................\n"

os.system("python "+test+"/../gaussian_bump.py "+data+"/gaussian_bump.nc")
os.system("grdmath "+data+"/gaussian_bump.nc 2 MUL = "+data+"/gaussian_bump_medium.nc")
os.system("grdmath "+data+"/gaussian_bump.nc 4 MUL = "+data+"/gaussian_bump_coarse.nc")


print "\n......................................................."

print ". Testing: annulus, Bsplines = True Compounds = False ."

print ".......................................................\n"

pytest.main(test+"/../annulus_bn.py")

print "\n......................................................."

print ". Testing: annulus, Bsplines = True Compounds = True  ."

print ".......................................................\n"

pytest.main(test+"/../annulus_by.py")

print "\n......................................................."

print ". Testing: annulus, Bsplines = False Compounds = True ."

print ".......................................................\n"

pytest.main(test+"/../annulus_ly.py")


print "\n......................................................."

print ".     Testing: BSplines = True Compounds = False      ."

print ".......................................................\n"

pytest.main(test+"/../bn.py")

print "\n......................................................."

print ".     Testing: BSplines = False Compounds = True      ."

print ".......................................................\n"

pytest.main(test+"/../ly.py")


print "\n......................................................."

print ".      Testing: BSplines = True Compounds = True      ."

print ".......................................................\n"

pytest.main(test+"/../by.py")

print "\nFinished Testing\n"
