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
is defined using define_id script

@author Varun Verma
"""

#import for message box to display error
from PyQt4.QtGui import QMessageBox

"""
This funcion writes teh physical surafces in the geo file. The id used for
the physical surface is the id from the shapefile which contains all the region
ids which distingueshes multiple domains
@param region_id_list    : specifies the ids of different surfaces in a list 
@param number_of_regions : specifies the number of different surfaces in the 
                           given domain data
@param geoFile           : file stream for the geo file to write the surfaces
"""
def __write_physical_surface_list(region_id_list,number_of_regions,geoFile) :
	unique_list = set(region_id_list)
	physical_id_dict = {}
	for i in range(number_of_regions-1):
		try :
			surface_ids = physical_id_dict[region_id_list[i]]
			surface_ids.append(i+1)
		except KeyError:
			physical_id_dict[region_id_list[i]] = [i+1]
	for k in physical_id_dict.keys():
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
This method writes the geo and physical ids using the helper emthods defined above.
This method makes sure there are no duplicate lines or points in the geo. The lines 
which are shared are only written once and the same id for the line is used anywhere
else where the same line is in the shape.
@param filepath : specifies the filepath of the geo file to be written
@param data     : specifies the data for teh domains, i.e. the ids and points
"""
def write_geo_file(filepath,data):
	region_id = data[0]
	shapes_index = data[1]
	boundary_id = data[2]
	domain_points = data[3]
	if ".geo" not in filepath :
		filepath += ".geo"
	#add the end of last shape to the shapes_index array
	shapes_index.append(len(domain_points))
	try:
		print "Writing Geo File..."
		#open the file to write the geo file
		geo = open(filepath,"w")
		#define the constants being used by the script
		point_dict = {}
		line_dict = {}
		line_loop_dict = {}
		line_index = -1
		surface_dict = {}

		line_num = 1
		line_loop_num = 1
		point_num = 1
		surface_num = 1

		#these are loop variants to access the current physical id of the line
		shape_number = -1
		for i in range(len(shapes_index)-1):
			surface_line_loops = []
			for line_loop in domain_points[shapes_index[i]:shapes_index[i+1]]:
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
						line_id = line_dict[tuple(points_in_line)]
						line_in_line_loop.append(line_id[0])
					except KeyError:
						try :
							#check if the line in opposite direction exists
							reverse_line = points_in_line + []
							reverse_line.reverse()
							line_id,line_p_id = line_dict[tuple(reverse_line)]
							line_in_line_loop.append(0-line_id)
						except KeyError:
							#if the line has not yet been written then write the file
							line_p_id = boundary_id[shape_number][line_index]
							line_dict[tuple(points_in_line)] = (line_num,line_p_id)
							line_in_line_loop.append(line_num)
							geo.write("Line(%i) = {%s};\n" %(line_num,str(points_in_line)[1:-1]))
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
			surface_num += 1
		__write_physical_surface_list(region_id,len(shapes_index),geo)
		__write_physical_lines_to_geo(line_dict.values(),geo)
		geo.close()

		print "Geo File Written: " + filepath
		print "Number of Surfaces Created: " + str(surface_num - 1)
	except IOError:
		print "Error: An error occurred while writing the geo file"
		QMessageBox.critical(None,"Error: In Writing Geo File","An error has occurred while writing the geo file")
		raise AssertionError


"""
This method uses a text file generated by the data given from the define id script.
"""
def test_with_txt_file():
	filepath = "shapefile_data.txt"
	data = open(filepath,"r")
	lines = data.readlines()
	data = [lines[1],lines[4],lines[7],lines[10]]
	data = map(eval,data)
	write_geo_file("/antartica_multiple_domain.geo",data)

