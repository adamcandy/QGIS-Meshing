import os, sys

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/testing_modules/'))
from helper_module import generate_files, make_directory

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/testing_modules/'))

from test_msh import mesh_file_test
from test_geo import geo_files_test


test = os.path.dirname(os.path.realpath(__file__)) + "/output"
support_file_path = os.path.dirname(os.path.realpath(__file__)) + "/support"


########################### APPLY YOUR CHANGES HERE: ##########################

fname = "test_ids" # just the name, no forward or backslashes!
command =	"-l LN --mesh --id idfile.shp domain.shp" # see modular_meshing.py for help

###############################################################################

generate_files(fname, command)



def test_annulus_bn_geo():
  curr_file = os.path.dirname(os.path.realpath(__file__)) + "/output/" + fname + "/" + fname + ".geo"

  assert geo_files_test(curr_file),"%s does not match the model answer" % (ntpath.basename(curr_file).rstrip())


def test_annulus_bn_msh():
  curr_file = os.path.dirname(os.path.realpath(__file__)) + "/output/" + fname + "/" + fname + ".msh"

    assert mesh_file_test(curr_file),"%s does not match the model answer" % (ntpath.basename(curr_file).rstrip())


############################# ADD MORE TESTS HERE: ############################
