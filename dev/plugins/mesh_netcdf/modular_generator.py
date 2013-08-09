import os
import glob
import pytest
import time

pwd = os.path.dirname(os.path.realpath(__file__))
test = pwd+"/../../tests/output"
support_files = pwd+"/../../tests/support"

print "\n......................................................."

print ".           Generating data: Gaussian bump            ."

print ".......................................................\n"

os.system("python "+test+"/../gaussian_bump.py "+support_files+"/gaussian_bump.nc")
os.system("grdmath "+support_files+"/gaussian_bump.nc 2 MUL = "+support_files+"/gaussian_bump_medium.nc")
os.system("grdmath "+support_files+"/gaussian_bump.nc 4 MUL = "+support_files+"/gaussian_bump_coarse.nc")


testfiles = glob.glob(pwd + "/../../tests/*.py")

pytest.main(testfiles)

