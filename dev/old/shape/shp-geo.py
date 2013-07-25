# Take in the shapefile given and convert to .geo file.

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

import shapefile
import matplotlib.pyplot as pyplot

# Read .shp file.
r = shapefile.Reader("large-area")

# Take in the shape info of the objects.
shapes = r.shapes()
print shapes[0].points

for j in range(len(shapes[0].parts)-1):
	x = []; y = []
	for i in range(shapes[0].parts[j], shapes[0].parts[j + 1]):
		x.append(shapes[0].points[i][0]); 	y.append(shapes[0].points[i][1])
		pyplot.plot(x, y)


x = []; y = []
for i in range(shapes[0].parts[0], shapes[0].parts[1]):
	x.append(shapes[0].points[i][0]); 	y.append(shapes[0].points[i][1])
	pyplot.plot(x, y)

pyplot.show()


"""
# Arbitrarily pick the 4th entry.
#Write the .geo file from the data read.
target = open("python.geo", "w") # Creates python.geo file to write to.
for i in range(len(shapes[3].points)):
	target.write('Point(%d) = {%.3f, %.3f, 0, %.3f};\n' %(i + 1, shapes[3].points[i][0], shapes[3].points[i][1], 1.0))
target.close()
"""
