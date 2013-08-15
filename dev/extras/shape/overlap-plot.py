# Take collection of circles, see which overlap then plot the shapes with the amended overlaps.

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

from shapely.geometry import Polygon, Point
from shapely.ops import cascaded_union
from matplotlib import pyplot
from shapely.validation import explain_validity

# definses one polygon square.
plist = [[(0, 0), (0, 2), (2, 2),(2,0), (0,0)],[(0,1),(5,1),(5,1.5),(0,1.5),(0,1)]] 
# Take the points given and creates polygons.
polygons = [Polygon(plist[0]),Polygon(plist[1] ) ]

# See which circles overlap and store in list.
# a.intersects(b)
overlapping = []
for n in range(len(polygons) - 1):
	if polygons[n].intersects(polygons[n+1]) == True: 
		# Two if statements to make sure the same polygon isn't being entered more than once.
		if polygons[n] not in overlapping: overlapping.append(polygons[n]) 
		if polygons[n + 1] not in overlapping: overlapping.append(polygons[n + 1]) 

# Create a new shape from the overlain circles.
join = cascaded_union(overlapping)

# Take the coords. of the perimeter of this new shape.
coords = list(join.exterior.coords)

# Store x-y coords of the perimeter in two lists to plot.
x = []; y = []
for i in range(len(coords)):
	x.append(coords[i][0]); y.append(coords[i][1])

# Plot results.
print coords
pyplot.plot(x, y)
#pyplot.xlim(-4, 4)
#pyplot.ylim(-4, 4)
pyplot.show()
