"""

##########################################################################
#  
#  QGIS-meshing plugins.
#  
#  Copyright (C) 2012-2013 Imperial College London and others.
#  
#  Please see the AUTHORS file in the main source directory for a
#  full list of copyright holders.
#  
#  Dr Adam S. Candy, adam.candy@imperial.ac.uk
#  Applied Modelling and Computation Group
#  Department of Earth Science and Engineering
#  Imperial College London
#  
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation,
#  version 2.1 of the License.
#  
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#  
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307
#  USA
#  
##########################################################################

This script writes the geo file. This script works with multiple domains and the surface id for that domain
is same as the id for the shape file in the shapefile. This script also respects the physical line id which 
is defined using define_id script.

This script has an option to allow the user to choose if BSpline or Line has to be used. Anotehr option is
to enable compound lines.

@author Varun Verma
"""

#might change to arrays, but extreamly quick anyway

#import for message box to display error
from PyQt4.QtGui import QMessageBox
import numpy as np
import numpy.lib.arraysetops as nset

"""
This funcion writes the physical surafces in the geo file. The id used for
the physical surface is the id from the shapefile which contains all the region
ids which distingueshes multiple domains
@param region_id_list    : specifies the ids of different surfaces in a list 
@param number_of_regions : specifies the number of different surfaces in the 
                           given domain data
@param geoFile           : file stream for the geo file to write the surfaces
"""
def __write_physical_surface_list(region_id_list,number_of_regions,geoFile) :#why two physical surface calls?
	unique_list = set(region_id_list)
	physical_id_dict = {}
	for i in range(number_of_regions-1):
		try :
			surface_ids = physical_id_dict[region_id_list[i]]
			surface_ids.append(i+1)
		except KeyError:
			physical_id_dict[region_id_list[i]] = [i+1]
		for k in physical_id_dict.keys():#implies physical_id_dict has multiple instances of k
			geoFile.write("Physical Surface(%i) = {%s};\n" % (k,str(physical_id_dict[k])[1:-1]))

"""
This method writes the physical line ids for individual lines in teh given domain data.
This method uses a helper method second which returns the second element in the tuple
@param lines_ids : list of tuples which consists of the id for the line and the physical
                   id for the line
@param geoFile   : file stream for the geo file to write the physical lines
"""
def __write_physical_lines_to_geo(lines_ids, geoFile):
 	def second(a):
		return a[1]
											
	line_numbers = lines_ids[0]
	unique_pid_list = set(map(second,lines_ids))
	physical_line_id_dict = {}
	for pid in unique_pid_list:
		physical_line_id_dict[pid] = []
	for line,pid in lines_ids:
		physical_line_id_dict[pid].append(line)
	for i in range(len(physical_line_id_dict.keys())):
		geoFile.write("Physical Line(%i) = {%s};\n" % (physical_line_id_dict.keys()[i],str(physical_line_id_dict.values()[i])[1:-1]))


"""
This funcion writes the physical surfaces in the geo file. The id used for
the physical surface is the id from the shapefile which contains all the region
ids which distingueshes multiple domains.
@param region_id_list    : specifies the ids of different surfaces in a list 
@param geoFile           : file stream for the geo file to write the surfaces
"""
def __write_physical_compound_surface_list(region_id_dict,geoFile) : #this is probably wrong
	for key in region_id_dict.keys():
		geoFile.write("Physical Surface(%i) = {%s};\n" % (key,str(region_id_dict[key])[1:-1]))

"""
This method writes the physical line ids for individual compound lines in the 
given domain data.
@param lines_ids : list of tuples which consists of the id for the line and the physical
                   id for the line
@param geoFile   : file stream for the geo file to write the physical lines
"""
def __write_physical_compound_lines_to_geo(lines_ids, geoFile):
	for key in lines_ids.keys():
		geoFile.write("Physical Line(%i) = {%s};\n" % (key,str(lines_ids[key])[1:-1]))


"""
This method is called when any line is written to a geo. This method checks if a new compound line
has to be written and operates accordingly. 
@param line_pid						: specifies the phsyical line id of the current line
@param prev_line_pid			: specifies the physical line if of the previous line
@param geo								: specifies the file stream for the file being written
@param line_num						: specifies the loop variant for the line id number
@param compound_line			:	specifies an array containing the line id of the lines
														to be included in the current compound line
@param line_id						: specifies the line id for the line which has just been written
@param compound_line_dict : specifies the dictionary containing compounds lines
														and there physical line id
@return										: returns the if of the current line, updated line_num,
														and the array compound_line
"""
def __check_for_compound_line_and_add(line_pid, prev_line_pid, geo, line_num, compound_line, line_id, compound_line_dict):
	if not compound_line :
		#if there are no lines in the current compound line then its the first line
		compound_line = [line_num]
	elif line_pid != prev_line_pid:
		#when the id of current line is changed, i.e. a new compound line has to be started
		line_num += 1
		#put the created compound line in the dict for the physical line to be written
		compound_line_dict[(line_num,prev_line_pid)] = compound_line + []
		#add the current line since it has a different physical id
		compound_line = [line_num-1]
	else :
		#writing to the same compound line
		compound_line.append(line_id)
	return line_pid, line_num, compound_line


"""
This method is to be implemented and would carry out the intersection
"""
def __check_for_intersection(arr1,arr2):
	inset = nset.intersect1d_nu(arr1,arr2)
	print inset
	if inset.size == 0:
		return [], [], [], [], [], [], []
	apre = arr1[:arr1.index(inset[0])]; apo = arr1[arr1.index(inset[-1]):]
	bpre = arr2[:arr2.index(inset[0])]; bpo = arr2[arr2.index(inset[-1]):]
	ra = range(arr1.index(inset[0]),arr1.index(inset[-1]))
	rb = range(arr2.index(inset[0]),arr2.index(inset[-1]))
	for i in ra: #vectorize/map
		con = 0
		con_s = 0
		flp = 0
		a1l = [[]]
		s1l = [[]]
		if i in inset:
			if flp == 1:
				flp = 0
				con_s += 1
				s1l.append([])
			s1l[con_s] = arr1[i]
			continue
		if flp == 0:
			flp = 1
			con += 1
			a1l.append([])
		a1l[con] = arr1[i]
	for i in rb:
		con = 0
		con_s = 0
		flp = 0
		b1l = [[]]
		if i in inset:
			continue
		if flp == 0:
			flp = 1
			con += 1
			b1l.append([])
		b1l[con] = arr2[i]
	return apre, a1l, apo, s1l, bpre, b1l, bpo

"""
this method splits the compound lines for multiple region which have adjacent boundaries
"""
def _iterator_for_compounds(line_num, compound_line_dict, keys, i, j, arr1, arr2 = [] ):
	compound_line_dict[keys[j]] = arr2
	compound_line_dict[(line_num,keys[i][1])] = arr1
	line_num += 1
	return line_num, compound_line_dict
	
def __split_compound_lines_for_multiple_regions(compound_line_dict,line_num):#multiple list instances might still give an error
	keys = compound_line_dict.keys()
	values = compound_line_dict.values()
	for i in range(len(keys)):
		for j in range(i+1,len(keys)):
				apre, a1l, apo, s1l, bpre, b1l, bpo = __check_for_intersection(values[i],values[j])
				if s1l == []:
					return compound_line_dict,line_num
				line_num, compound_line_dict = map(_iterator_for_compounds( line_num, compound_line_dict, keys, i, j, s1l ), s1l) #possibly change to vectorize at some point
				line_num, compound_line_dict = map(_iterator_for_compounds( line_num, compound_line_dict, keys, i, j, bpre, apre ), bpre, apre)
				line_num, compound_line_dict = map(_iterator_for_compounds( line_num, compound_line_dict, keys, i, j, b1l, a1l ), b1l, a1l)
				line_num, compound_line_dict = map(_iterator_for_compounds( line_num, compound_line_dict, keys, i, j, bpo, apo), bpo, apo)
	return compound_line_dict

"""
this method writes the compound line to the geo file

"""
def __write_compound_lines(compound_dict, geo):
	for i in range(len(compound_dict.keys())):
		geo.write("Compound Line(%i) = {%s};\n"%(compound_dict.keys()[i][0],str(compound_dict.values()[i])[1:-1]))

"""
This method writes the geo and physical ids using the helper emthods defined above.
This method makes sure there are no duplicate lines or points in the geo. The lines 
which are shared are only written once and the same id for the line is used anywhere
else where the same line is in the shape.
@param filepath : specifies the filepath of the geo file to be written
@param data     : specifies the data for the domains, i.e. the ids and points
"""
def write_geo_file(filepath,data, compound_line_enable, use_bspline):
	def __remove_last_line_using_same_point(lines):
		last = lines[-1]
		if last[0]==last[1]:
			lines.pop()
		return lines
	region_id = data[0]
	#compound_line_enable = True
	#use_bspline = False
	
	if use_bspline:
		line_string = "BSpline"
	else:
		line_string = "Line"

	shapes_index = data[1]
	boundary_id = data[2]
	domain_points = data[3]
	#remove the last line which has same point twice
	map(__remove_last_line_using_same_point, domain_points)
	if ".geo" not in filepath:
		filepath += ".geo"

	#add the end of last shape to the shapes_index array
	shapes_index.append(len(domain_points))
	try:
		#open the file to write the geo file
		geo = open(filepath,"w")
		print "Writing geo file"
		#define the loop variants being used by the following
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
		shape_number = -1

		#loop for every shape. each shape contains some islands so split points are used
		for i in range(len(shapes_index)-1):
			surface_line_loops = []
			#loop for every line loop in each shape. i.e. boundary and islands
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
							#check if the current point already exists
							point_id = point_dict[tuple(p)]
							points_in_line.append(point_id)
						except KeyError:
							#write the point to geo file and add it to the dictionary
							point_dict[tuple(p)] = point_num
							points_in_line.append(point_num)
							geo.write("Point(%i) = {%s,0};\n"%(point_num, str(p)[1:-1]))
							point_num += 1
					try :
						#check if the current line has already been written
						line_id,line_pid = line_dict[tuple(points_in_line)]
						line_in_line_loop.append(line_id)
						#if compound lines are enabled then check for writing compound line
						if compound_line_enable:
							prev_line_pid,line_num, compound_line = __check_for_compound_line_and_add(line_pid,prev_line_pid,
								geo, line_num, compound_line,	line_id, compound_line_dict)
					except KeyError:
						try :
							#check if the line in opposite direction exists
							reverse_line = points_in_line + []
							reverse_line.reverse()
							line_id,line_pid = line_dict[tuple(reverse_line)]
							line_in_line_loop.append(0-line_id)
							if compound_line_enable:
								prev_line_pid,line_num, compound_line = __check_for_compound_line_and_add(line_pid, 
									prev_line_pid, geo, line_num, compound_line,line_id, compound_line_dict)
						except KeyError:
							#if the line has not yet been written then write the file and add to the dictionary
							line_pid = boundary_id[shape_number][line_index]
							line_dict[tuple(points_in_line)] = (line_num,line_pid)
							line_in_line_loop.append(line_num)
							geo.write("%s(%i) = {%s};\n" %(line_string, line_num,str(points_in_line)[1:-1]))
							if compound_line_enable:
								prev_line_pid,line_num, compound_line = __check_for_compound_line_and_add(line_pid, 
									prev_line_pid, geo, line_num, compound_line,line_num, compound_line_dict)
							line_num += 1
				#write the closing compound line
				if compound_line_enable:
					compound_line_dict[(line_num,prev_line_pid)] = compound_line + []
					line_num += 1
				try:
					#check if the current line loop already exists
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
						#write a new line loop
						line_loop_dict[tuple(line_in_line_loop)] = line_loop_num
						surface_line_loops.append(line_loop_num)
						geo.write("Line Loop(%i) = {%s};\n" % (line_loop_num,str(line_in_line_loop)[1:-1]))
						line_loop_num += 1
			surface_pid = region_id[shapes_index[i]]
			try :
				surface_pid_list = surface_dict[surface_pid]
				surface_pid_list.append(surface_num)
			except KeyError:
				surface_dict[surface_pid] = [surface_num]

			geo.write("Plane Surface(%i) = {%s};\n" % (surface_num,str(surface_line_loops)[1:-1]))
			
			#if compound_line_enable:
				#geo.write("Compound Surface(%i) = {%i};\n" % (surface_num + 1, surface_num))
				#surface_num +=1
				#try :
					#surface_lists = compound_surface_dict[region_id[shapes_index[i]]]
					#surface_lists.append(surface_num)
				#except KeyError:
					#compound_surface_dict[region_id[shapes_index[i]]] = [surface_num]
			#else:
			surface_num +=1
		if compound_line_enable:
			#A method to split the compound lines would be called here
			
			if len(shapes_index)>1:
				compound_line_dict = __split_compound_lines_for_multiple_regions(compound_line_dict,line_num)
			__write_compound_lines(compound_line_dict,geo)
			__write_physical_lines_to_geo(compound_line_dict.keys(), geo)
			__write_physical_surface_list(region_id, len(shapes_index), geo)#posibly this
			#__write_physical_compound_surface_list(compound_surface_dict, geo)#may remove
		else :
			__write_physical_lines_to_geo(line_dict.values(),geo)
			__write_physical_surface_list(region_id, len(shapes_index), geo)

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
