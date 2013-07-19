from parser_class import MeshData
import py
import glob


# used too pass arguments to the test function
def pytest_generate_tests(metafunc):
    # called once per each test function
    for funcargs in metafunc.cls.params[metafunc.function.__name__]:
        # schedule a new test function run with applied **funcargs
        metafunc.addcall(funcargs=funcargs)


class TestClass:
	#parameters to the test function
    params = {
        'test_msh_files': [dict(curr_file=x) for x in glob.glob("../../tests/*.msh")],
    }

    def test_msh_files(self, curr_file):

    	index = len(curr_file) - 1
        curr = curr_file[index]

        # retrieve just the file name from the path
        while index > 0 and curr != '/':

            index -= 1
            curr = curr_file[index]


        index -= 1
        fname = curr_file[index : len(curr_file)]

        assert mesh_file_test(curr_file),"%s does not match the model answer" % (fname)


# Compares given file with the model answer. Throws an AssertionError if the files don't match
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

	#parse the file being tested and the model answer
	model_answer.parse()
	tested_answer.parse()

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


# compares the nodes in the tested and model answer files. First it looks for
# the identical nodes, if found deletes them off the longer dictionary,
# otherwise adds to a 'wait_list'. This is to speed up the process of testing.
def compare_nodes(shorter_dict, longer_dict) :

	wait_list = {}

	for key in shorter_dict :

		if key in longer_dict and shorter_dict[key] == longer_dict[key] :
			#remove and continue
			del(longer_dict[key])

		else :
			wait_list[key] = shorter_dict[key] # add it to waiting dictionary

	# need to check the wait list if theres any matches
	return check_nodes_wait_list(wait_list, longer_dict)


# go through all keys in the wait_list dictionary and compare to model answer (here: comp dictioary)
# if they are within +/- 5 delete off the comp dictionary
def check_nodes_wait_list(wait_list, comp) :

	for key in wait_list :

		for comp_key in comp :

			if (float(comp_key) + 5.0) >= float(key) >= (float(comp_key) - 5.0)  and (float(comp[comp_key]) + 5.0) >= float(wait_list[key]) >= (float(comp[comp_key]) - 5.0) :
				del(comp[comp_key])
				break
			else :
				return False
	return True


# compares the elements in the tested and model answer files. First it looks for
# the identical elements, if found deletes them off the longer list,
# otherwise adds to a 'wait_list'. This is to speed up the process of testing.
def compare_elements(shorter_list, longer_list) :

	wait_list = []

	c = 0
	for tuple1 in shorter_list :
		c += 1

		if tuple1 in longer_list :
			longer_list.remove(tuple1)
		else :
			wait_list.append(tuple1)

	return check_elems_wait_list(wait_list, longer_list)


# go through all keys in the wait_list and compare to model answer (here: comp list)
# if they are within ................... delete off the comp list
def  check_elems_wait_list(wait_list, comp):

	for elem in wait_list :

		for comp_elem in comp :

			if True :
				print "REMEMBER TO FINISH THIS!!!!!!!!!!!!!!!!!!!!!"
			else :
				return False
	return True

