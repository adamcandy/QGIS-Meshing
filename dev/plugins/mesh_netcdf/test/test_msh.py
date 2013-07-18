from parser_class import MeshData
# content of test_expectation.py
import py
import glob


def pytest_generate_tests(metafunc):
    # called once per each test function
    for funcargs in metafunc.cls.params[metafunc.function.__name__]:
        # schedule a new test function run with applied **funcargs
        metafunc.addcall(funcargs=funcargs)

class TestClass:
    params = {
        'test_msh_files': [dict(a=x) for x in glob.glob("../../tests/*.msh")],
    }

    def test_msh_files(self, a):

    	index = len(a) - 1
        curr = a[index]

        # retrieve just the file name from the path
        while index > 0 and curr != '/':

            index -= 1
            curr = a[index]


        index -= 1
        fname = a[index : len(a)]

        assert mesh_file_test(a),"%s does not match the model answer" % (fname)



# Compares given file with the model answer
def mesh_file_test(file_path) :

	index = len(file_path) - 1
	curr = file_path[index]

	# retrieve just the file name from the path
	while index > 0 and curr != '/':

		index -= 1
		curr = file_path[index]


	fname = file_path[index : len(file_path)]


	#get filepath of the correct model answer
	model_answer = MeshData("../../tests/model_answers/" + fname)
	tested_answer = MeshData(file_path)

	model_answer.parse()
	tested_answer.parse()

	print "checking meshes ..."


	if model_answer.number_of_nodes > tested_answer.number_of_nodes :
		#model answer has more nodes
		if compare_nodes(tested_answer.node_dict, model_answer.node_dict) :

			if model_answer.number_of_elems > tested_answer.number_of_elems :
				# model answer has more elems
				return compare_elements(tested_answer.elems_list, model_answer.elems_list)
			else :
				# tested answer has more elems
				return compare_elements(model_answer.elems_list, tested_answer.elems_list)

	else :
		# tested answer has more nodes
		if compare_nodes(model_answer.node_dict, tested_answer.node_dict) :

			if model_answer.number_of_elems > tested_answer.number_of_elems :
				# model answer has more elems
				return compare_elements(tested_answer.elems_list, model_answer.elems_list)
			else :
				# tested answer has more elems
				return compare_elements(model_answer.elems_list, tested_answer.elems_list)

	return False


def compare_nodes(shorter_dict, longer_dict) :
	print "in comp nodes..."

	wait_list = {}

	for key in shorter_dict :

		if key in longer_dict and shorter_dict[key] == longer_dict[key] :
			#remove and continue
			del(longer_dict[key])

		else :
			wait_list[key] = shorter_dict[key] # add it to waiting dictionary

	# need to check the wait list if theres any matches
	return check_nodes_wait_list(wait_list, longer_dict)


def check_nodes_wait_list(wait_list, comp) :

	# go through all keys in dict and compare to model (here: comp)
	# if withi +/- 5 delete off longer
	print wait_list
	print comp

	print "in check wait_list"

	for key in wait_list :

		for comp_key in comp :

			if (float(comp_key) + 5.0) >= float(key) >= (float(comp_key) - 5.0)  and (float(comp[comp_key]) + 5.0) >= float(wait_list[key]) >= (float(comp[comp_key]) - 5.0) :
				print "yes"

				del(comp[comp_key])
				break
			else :
				print "no"
				return False
	return True


# WILL NEED TO ACCEPT SIMILAR INPPUTS (As opp to IDENTICAL)
def compare_elements(shorter_list, longer_list) :
	print "in comp elems"

	wait_list = []

	c = 0
	for tuple1 in shorter_list :
		print "looking for potential matches" + str(c)

		c += 1

		if tuple1 in longer_list :
			print  str(tuple1)
			longer_list.remove(tuple1)
		else :
			wait_list.append(tuple1)

	return check_elems_wait_list(wait_list, longer_list)

def  check_elems_wait_list(wait_list, comp):

	print "......................"
	print wait_list
	print comp


	for elem in wait_list :

		for comp_elem in comp :

			if True :
				print "REMEMBER TO FINISH THIS!!!!!!!!!!!!!!!!!!!!!"
			else :
				return False
	return True

