import sys, os

from test_msh import mesh_file_test
from test_geo import geo_files_test

class Class() :


	def __init__(self, fname) :
		self.fname = fname



	def test_annulus_bn_geo(self):
		curr_file = os.path.dirname(os.path.realpath(__file__)) + "/../output/" + self.fname + "/" + self.fname + ".geo"

		assert geo_files_test(curr_file),"%s does not match the model answer" % (ntpath.basename(curr_file).rstrip())




	def test_annulus_bn_msh(self):
		curr_file = os.path.dirname(os.path.realpath(__file__)) + "/../output/" + self.fname + "/" + self.fname + ".msh"

		assert mesh_file_test(curr_file),"%s does not match the model answer" % (ntpath.basename(curr_file).rstrip())
