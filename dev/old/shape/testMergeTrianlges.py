from shapely.ops import cascaded_union

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

from shapely.geometry import *
import sys
import matplotlib.pyplot as pyplot

t1 = Polygon([(0,0),(1,1),(2,0),(0,0)])
t2 = Polygon([(2,0),(1,1),(2,2),(2,0)])
pts = [[[4,0],[3,1],[4,2],[4,0]],[[0,0],[1,1],[2,0],[0,0]],[[2,4],[3,3],[4,4],[2,4]],[[0,2],[1,3],[0,4],[0,2]],[[2,2],[3,1],[4,2],[2,2]],[[2,0],[3,1],[2,2],[2,0]],[[2,2],[3,3],[4,2],[2,2]],[[2,0],[1,1],[2,2],[2,0]],[[2,2],[3,3],[2,4],[2,2]],[[0,2],[1,1],[2,2],[0,2]],[[0,2],[1,3],[2,2],[0,2]],[[2,2],[1,3],[2,4],[2,2]],[[0,0],[1,1],[0,2],[0,0]],[[2,0],[3,1],[4,0],[2,0]],[[0,4],[1,3],[2,4],[0,4]],[[4,2],[3,3],[4,4],[4,2]]]
polygons = []
for p in pts : 
	polygons.append(Polygon(p))
u = cascaded_union(polygons)
print u.geom_type
points = list(u.exterior.coords)
print points
x = []
y = []
for p in points:
	x1,y1=p
	x.append(x1)
	y.append(y1)
pyplot.plot(x,y)
pyplot.show()
sys.exit()
for l in u.geoms :
	print(list(l.coords))
