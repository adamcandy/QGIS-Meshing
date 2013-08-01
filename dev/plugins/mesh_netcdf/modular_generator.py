import os
import glob
import pytest
import time

pwd = os.path.dirname(os.path.realpath(__file__))
test = pwd+"/../../tests/output"
data = pwd+"/../../tests/support"

start = time.time()


print "\n......................................................."

print ".           Generating data: Gaussian bump            ."

print ".......................................................\n"

os.system("python "+test+"/../gaussian_bump.py "+data+"/gaussian_bump.nc")
os.system("grdmath "+data+"/gaussian_bump.nc 2 MUL = "+data+"/gaussian_bump_medium.nc")
os.system("grdmath "+data+"/gaussian_bump.nc 4 MUL = "+data+"/gaussian_bump_coarse.nc")



print '\033[1m' + " \nGenerating tests: annulus, Bsplines = True Compounds = False\n " + '\033[0m'

pytest.main([test+"/../annulus_bn.py"])

print '\033[1m' + " \nGenerating tests: annulus, Bsplines = True Compounds = True\n " + '\033[0m'

pytest.main([test+"/../annulus_by.py"])

print '\033[1m' + " \nGenerating tests: annulus, Bsplines = False Compounds = True \n " + '\033[0m'

pytest.main([test+"/../annulus_ly.py"])

print '\033[1m' + " \nGenerating tests: BSplines = True Compounds = False\n " + '\033[0m'

pytest.main([test+"/../bn.py"])

print '\033[1m' + " \nGenerating tests: Testing: BSplines = False Compounds = True\n " + '\033[0m'

pytest.main([test+"/../ly.py"])

print '\033[1m' + " \nGenerating tests: BSplines = True Compounds = True\n " + '\033[0m'

pytest.main([test+"/../by.py"])

end = time.time()

print '\033[1m' + " \nFinished testing in %.2f seconds\n "%(end - start) + '\033[0m'
