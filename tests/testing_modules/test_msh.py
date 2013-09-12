from parser_class import MeshData
from collections import defaultdict
import py
import glob
import os
import ntpath


pwd = os.path.dirname(os.path.realpath(__file__))


# Compares given file with the model answer. Returns False if the files do not match
def mesh_file_test(file_path) :

	fname = ntpath.basename(file_path).rstrip()


	#get filepath of the correct model answer
	model_answer = MeshData(file_path.replace("output", "model_answers", 1))
	tested_answer = MeshData(file_path)

	#parse the file being tested and the model answer
	model_answer.parse()
	tested_answer.parse()

	if model_answer.number_of_nodes > tested_answer.number_of_nodes :
		#model answer has more nodes
		return compare_nodes(tested_answer.node_dict, model_answer.node_dict)
	else :
		# tested answer has more nodes
		return compare_nodes(model_answer.node_dict, tested_answer.node_dict)

	return False


# compares the nodes in the tested and model answer files. First it looks for
# the identical nodes, if found deletes them off the longer dictionary,
# otherwise adds to a 'wait_list'. This is to speed up the process of testing.
def compare_nodes(shorter_dict, longer_dict) :

	wait_list = defaultdict(list)

	for key in shorter_dict :

		if key in longer_dict and shorter_dict[key] == longer_dict[key] :
			#remove and continue
			del(longer_dict[key])


		elif key in longer_dict:

			for item in shorter_dict[key] :
				if item in longer_dict[key] :
					longer_dict[key].remove(item)
				else :
					wait_list[key].append(item) # add it to waiting dictionary
					pass

	return check_nodes_wait_list(wait_list, longer_dict)


# go through all keys in the wait_list dictionary and compare to model answer
# (here: comp dictioary) if they are within +/- 2 delete off the comp dictionary
def check_nodes_wait_list(wait_list, comp) :

	matched = False

	for key in wait_list :

		for comp_key in comp :


			if close_to(float(comp_key), float(key), 2) :

				# check the value lists
				matched = True

				if compare_sets(wait_list[key], comp[comp_key]) :
					del comp[comp_key]
					break

		if not matched :
			return False
		else :
			matched = False

	return True


# checks whether 2 sets are similar. First orders the sets, then checks whether
# all the values in the shorter set have a value similar to each of them in the
# longer set.
def  compare_sets(set1, set2):

	if len(set1) > len(set2) :
		longer = set1
		shorter = set2
	else :
		longer = set2
		shorter = set1


	longer.sort(key=float)
	shorter.sort(key=float)

	discarded = False

	for shorter_set_item in shorter :
		if shorter_set_item in longer :
			longer.remove(shorter_set_item)
			discarded = True
			break
		else :
			for longer_set_item in longer :
				if close_to(float(shorter_set_item), float(longer_set_item), 2) :
					longer.remove(longer_set_item)
					discarded = True
					break
			if not discarded :
				return False
			else :
				discarded = False

	return True


# checks whether two first argumets are withi 'amount' from each other.
def close_to(first, second, amount) :
	return abs(first - second) <= amount