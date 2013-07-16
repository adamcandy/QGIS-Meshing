from mesh_test import mesh_file_test


def test_msh(filename) :

	print "in here!!"

	assert(mesh_file_test(filename)), "%s does not match the model answer" % (filename)




#all_files = glob.glob("../../tests/*.msh")
#
#for fname in all_files :
#	print "!"
test_msh("ref.msh")
#	print "."