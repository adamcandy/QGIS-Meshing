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

pytest.main([test+"/../test_annulus_BSplines.py"])

print '\033[1m' + " \nGenerating tests: annulus, Bsplines = True Compounds = True\n " + '\033[0m'

pytest.main([test+"/../test_annulus_BSplines_Compound_lines.py"])
pytest.main([test+"/../test_annulus_BSplines_Compound_lines_coarse_metric.py"])
pytest.main([test+"/../test_annulus_BSplines_Compound_lines_medium_metric.py"])
pytest.main([test+"/../test_annulus_BSplines_Compound_lines_metric.py"])

print '\033[1m' + " \nGenerating tests: annulus, Bsplines = False Compounds = True \n " + '\033[0m'

pytest.main([test+"/../test_annulus_Compound_lines.py"])
pytest.main([test+"/../test_annulus_Compound_lines_coarse_metric.py"])
pytest.main([test+"/../test_annulus_Compound_lines_medium_metric.py"])
pytest.main([test+"/../test_annulus_Compound_lines_metric.py"])

print '\033[1m' + " \nGenerating tests: BSplines = True Compounds = False\n " + '\033[0m'

pytest.main([test+"/../test_BSplines_0.py"])
pytest.main([test+"/../test_BSplines_1.py"])
pytest.main([test+"/../test_BSplines_2.py"])
pytest.main([test+"/../test_BSplines_3.py"])

print '\033[1m' + " \nGenerating tests: Testing: BSplines = False Compounds = True\n " + '\033[0m'

pytest.main([test+"/../test_Compound_lines_0.py"])
pytest.main([test+"/../test_Compound_lines_1.py"])
pytest.main([test+"/../test_Compound_lines_2.py"])
pytest.main([test+"/../test_Compound_lines_3.py"])

print '\033[1m' + " \nGenerating tests: BSplines = True Compounds = True\n " + '\033[0m'

#pytest.main([test+"/../test_BSplines_Compound_lines_0.py"])
pytest.main([test+"/../test_BSplines_Compound_lines_1.py"])
pytest.main([test+"/../test_BSplines_Compound_lines_2.py"])
#pytest.main([test+"/../test_BSplines_Compound_lines_3.py"])

end = time.time()

print '\033[1m' + " \nFinished testing in %.2f seconds. \n\nFor gmsh output please see the output.log file located at: %s\n "%(end - start, pwd) + '\033[0m'
