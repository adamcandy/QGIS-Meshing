import shapefile

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

import matplotlib.pyplot as pyplot
import sys

sf = shapefile.Reader(sys.argv[1])
shapes = sf.shapes()
print(shapes[0].shapeType)
#print(shapes[0].points)
print(shapes[0].parts)
print(shapes[0].points)
i = -1
for s in shapes:
	points = s.points
	x = []
	y = []
	print("shp start")
	for p in points:
		i+=1
		print("%d-->%s"%(i,p))
		x.append(p[0])
		y.append(p[1])
	pyplot.plot(x,y)

#pyplot.xlim(-1,5)
#pyplot.ylim(-1,5)
pyplot.show()
