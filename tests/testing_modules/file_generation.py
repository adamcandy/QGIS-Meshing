import os, sys

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../../plugins/mesh_netcdf/'))
from modular_meshing import Modular_meshing



def make_directory(fname) :

	pwd = os.path.dirname(os.path.realpath(__file__))

	if not os.path.exists(pwd +"/../output/" + fname):
	    os.makedirs(pwd +"/../output/" + fname)


def generate_files(fname, command) :

	make_directory(fname)

	os.system("python "+pwd+"/../../plugins/mesh_surface/mesh_surface "+command)

