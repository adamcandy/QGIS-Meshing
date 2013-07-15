from parser_class import MeshData
#main method called from outside. Compares given file with the model answer
def test_mesh_file(file_path) :


	index = len(file_path) - 1
	curr = file_path[index]

	# retrieve just the file name from the path
	while index > 0 and curr != '/':

		index -= 1
		curr = file_path[index]


	fname = file_path[index : len(file_path)]



	# find a way to get the right file! - last part of file_path strig or sth like that..
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


# WILL NEED TO ACCEPT SIMILAR INPPUTS (As opp to IDENTICAL)
def compare_nodes(shorter_dict, longer_dict) :
	print "in comp nodes..."


	#WOULD THIS WORK?
	for key in shorter_dict :

		if key in longer_dict :
			#remove and continue
#			del(longer_dict[key])
			pass
		else :
			# no match -> FAIL
			return False

	# found matches for all entries -> PASS
	return True




# WILL NEED TO ACCEPT SIMILAR INPPUTS (As opp to IDENTICAL)
def compare_elements(shorter_list, longer_list) :
	print "in comp elems"
	# go through the shorter list looking for each item in longer list.
	# potential_matches is a list of all tuples with the same first elem.
	c = 0
	for tuple1 in shorter_list :
		print "looking for potential matches" + str(c)

		c += 1

		if tuple1 in longer_list :
			print  str(tuple1)
			longer_list.remove(tuple1)
		else :
			return False


"""
		print "looking for potential matches" + str(c)
		c+=1
		#find all the potential matches
		potential_matches = [x for x in longer_list if tuple1[0] == x[0]]


		if len(potential_matches) == 0 :
			# no match -> FAIL
			return False
		elif tuple1 in potential_matches :
			#found a match -> remove it & continue
			longer_list.remove(tuple1)
		else :
			# no match -> FAIL
			return False

	# found matches for all tuples -> PASS
	return True
"""


print test_mesh_file("ref.msh")