"""
This script writes the geo file. This script works with multiple domains and the surface id for that domain
is same as the id for the shape file in the shapefile. This script also respects the physical line id which 
is defined using define_id script.

This script has an option to allow the user to choose if BSpline or Line has to be used. Anotehr option is
to enable compound lines.

@author Varun Verma
"""

#import for message box to display error
from PyQt4.QtGui import QMessageBox

"""
This funcion writes the physical surfaces in the geo file. The id used for
the physical surface is the id from the shapefile which contains all the region
ids which distingueshes multiple domains.
@param region_id_list    : specifies the ids of different surfaces in a list 
@param geoFile           : file stream for the geo file to write the surfaces
"""
def __write_physical_surface_list(region_id_dict,geoFile) :
	for key in region_id_dict.keys():
		geoFile.write("Physical Surface(%i) = {%s};\n" % (key,str(region_id_dict[key])[1:-1]))

"""
This method writes the physical line ids for individual compound lines in the 
given domain data.
@param lines_ids : list of tuples which consists of the id for the line and the physical
                   id for the line
@param geoFile   : file stream for the geo file to write the physical lines
"""
def __write_physical_lines_to_geo(lines_ids, geoFile):
	for key in lines_ids.keys():
		geoFile.write("Physical Line(%i) = {%s};\n" % (key,str(lines_ids[key])[1:-1]))


"""
This method is called when any line is written to a geo. This method
"""
def __write_compound_line(compound_line_empty, line_pid, prev_line_pid, geo, line_num, compound_line, line_id, compound_line_dict):
	if compound_line_empty:
		compound_line = [line_num]
	elif line_pid != prev_line_pid:
		line_num += 1
		geo.write("Compound Line(%i) = {%s};\n" % (line_num , str(compound_line)[1:-1]))
		#put the created compound line in the dict for the physical line to be written
		try :
			pid_list = compound_line_dict[prev_line_pid]
			pid_list.append(line_num)
		except KeyError:
			compound_line_dict[prev_line_pid] = [line_num]
		compound_line = [line_num-1]
	else :
		compound_line.append(line_id)
	prev_line_pid = line_pid
	return prev_line_pid, line_num, compound_line


"""
This method writes the geo and physical ids using the helper emthods defined above.
This method makes sure there are no duplicate lines or points in the geo. The lines 
which are shared are only written once and the same id for the line is used anywhere
else where the same line is in the shape.
@param filepath : specifies the filepath of the geo file to be written
@param data     : specifies the data for teh domains, i.e. the ids and points
"""
def write_geo_file(filepath,data):
	def __remove_last_line_using_same_point(lines):
		last = lines[-1]
		if last[0]==last[1]:
			lines.pop()
		return lines
	region_id = data[0]
	shapes_index = data[1]
	boundary_id = data[2]
	domain_points = data[3]
	map(__remove_last_line_using_same_point, domain_points)
	if ".geo" not in filepath:
		filepath += ".geo"
	#add the end of last shape to the shapes_index array
	shapes_index.append(len(domain_points))
	try:
		#open the file to write the geo file
		geo = open(filepath,"w")
		print "Writing geo file"
		#define the constants being used by the script
		point_dict = {}
		line_dict = {}
		line_loop_dict = {}
		line_index = -1
		surface_dict = {}
		compound_line_dict = {}
		compound_surface_dict = {}

		line_num = 1
		line_loop_num = 1
		point_num = 1
		surface_num = 1

		#these are loop variants to access the current physical id of the line
		shape_number = -1
		for i in range(len(shapes_index)-1):
			surface_line_loops = []
			for line_loop in domain_points[shapes_index[i]:shapes_index[i+1]]:
				compound_line = []
				prev_line_pid = -1
				shape_number += 1
				line_in_line_loop = []
				line_index = -1
				for line in line_loop:
					line_index += 1
					points_in_line = []
					for p in line:
						try:
							point_id = point_dict[tuple(p)]
							points_in_line.append(point_id)
						except KeyError:
							point_dict[tuple(p)] = point_num
							points_in_line.append(point_num)
							geo.write("Point(%i) = {%s,0};\n"%(point_num, str(p)[1:-1]))
							point_num += 1
					try :
						line_id,line_pid = line_dict[tuple(points_in_line)]
						line_in_line_loop.append(line_id)
						prev_line_pid,line_num, compound_line = __write_compound_line(not compound_line,line_pid,prev_line_pid,
								geo, line_num, compound_line,	line_id, compound_line_dict)
					except KeyError:
						try :
							#check if the line in opposite direction exists
							reverse_line = points_in_line + []
							reverse_line.reverse()
							line_id,line_pid = line_dict[tuple(reverse_line)]
							line_in_line_loop.append(0-line_id)
							prev_line_pid,line_num, compound_line = __write_compound_line(not compound_line, line_pid, 
									prev_line_pid, geo, line_num, compound_line,line_id, compound_line_dict)
						except KeyError:
							#if the line has not yet been written then write the file
							line_pid = boundary_id[shape_number][line_index]
							line_dict[tuple(points_in_line)] = (line_num,line_pid)
							line_in_line_loop.append(line_num)
							geo.write("Line(%i) = {%s};\n" %(line_num,str(points_in_line)[1:-1]))
							prev_line_pid,line_num, compound_line = __write_compound_line(not compound_line, line_pid, 
									prev_line_pid, geo, line_num, compound_line,line_num, compound_line_dict)
							line_num += 1
				geo.write("Compound Line(%i) = {%s};\n" % (line_num, str(compound_line)[1:-1]))
				try :
					pid_list = compound_line_dict[prev_line_pid]
					pid_list.append(line_num)
				except KeyError:
					compound_line_dict[prev_line_pid] = [line_num]
				line_num += 1
				try:
					line_loop_id = line_loop_dict[tuple(line_in_line_loop)]
					surface_line_loops.append(line_loop_id)
				except KeyError:
					#check for reverse line loop
					try :
						reverse_loop = line_in_line_loop + []
						reverse_loop.reverse()
						line_loop_id = line_loop_dict[tuple(reverse_loop)]
						surface_line_loops.append(0-line_loop_id)
					except KeyError:
						line_loop_dict[tuple(line_in_line_loop)] = line_loop_num
						surface_line_loops.append(line_loop_num)
						geo.write("Line Loop(%i) = {%s};\n" % (line_loop_num,str(line_in_line_loop)[1:-1]))
						line_loop_num += 1
			surface_dict[surface_num] = region_id[shapes_index[i]]
			geo.write("Plane Surface(%i) = {%s};\n" % (surface_num,str(surface_line_loops)[1:-1]))
			geo.write("Compound Surface(%i) = {%i};\n" % (surface_num + 1, surface_num))
			try :
				surface_lists = compound_surface_dict[region_id[shapes_index[i]]]
				surface_lists.append(surface_num+1)
			except KeyError:
				compound_surface_dict[region_id[shapes_index[i]]] = [surface_num + 1]
			surface_num += 2
		__write_physical_lines_to_geo(compound_line_dict ,geo)
		__write_physical_surface_list(compound_surface_dict, geo)
		geo.write("\n\nMesh.RemeshAlgorithm=1;\n")
		geo.close()
		print "geo file written : " + filepath
	except IOError:
		print "Error: An error occurred while writing the geo file"
		QMessageBox.critical(None,"Error: In Writing Geo File","An error has occurred while writing the geo file")
		raise AssertionError


"""
This method uses a text file generated by the data given from the define id script.
"""
def test_with_txt_file():
	filepath = "shapefile_data_simplified.txt"
	data = open(filepath,"r")
	lines = data.readlines()
	data = [lines[1],lines[4],lines[7],lines[10]]
	data = map(eval,data)
	write_geo_file("antartica_multiple_domain.geo",data)
