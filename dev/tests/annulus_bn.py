import os
import glob
import pytest
import sys
import ntpath

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/testing_modules/'))

from test_msh import mesh_file_test
from test_geo import geo_files_test

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../plugins/mesh_netcdf/'))

from modular_meshing import Modular_meshing


pwd = os.path.dirname(os.path.realpath(__file__))
test = pwd+"/output"
data = pwd+"/support"


def start() :

	if not os.path.exists(test +"/annulus_BN"):
	    os.makedirs(test +"/annulus_BN")

	Modular_meshing("--line BN -g "+test+"/annulus_BN/test_annulus_BN.geo "+data+"/annulus.shp --mesh --mval 10")

	print "......................................................"
	print '\033[1m' + " \nTesting: annulus, Bsplines = True Compounds = False\n " + '\033[0m'

start()

# used too pass arguments to the test function
def pytest_generate_tests(metafunc):
    # called once per each test function
    for funcargs in metafunc.cls.params[metafunc.function.__name__]:
        # schedule a new test function run with applied **funcargs
        metafunc.addcall(funcargs=funcargs)


class TestClass:
    """ Runs various tests on files """

    #parameters to the test function
    params = {

    	'test_annulus_bn_geo' : [dict(curr_file=x) for x in glob.glob(pwd +"/output/annulus_BN/*.geo")],
        'test_annulus_bn_msh': [dict(curr_file=x) for x in glob.glob(pwd +"/output/annulus_BN/*.msh")],
    }


    def test_annulus_bn_geo(self, curr_file):

		assert geo_files_test(curr_file),"%s does not match the model answer" % (ntpath.basename(a).rstrip())



    # Tests whether nodes of the file being are similar to the nodes in the
    # model answer. Throws an AssertionError if the files don't match
    def test_annulus_bn_msh(self, curr_file):

        assert mesh_file_test(curr_file),"%s does not match the model answer" % (ntpath.basename(curr_file).rstrip())
