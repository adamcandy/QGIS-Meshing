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

x = -100
y = 50
w = shapefile.Writer(shapeType=5)
##w.poly(parts = [[[x,x],[x,y],[y,y],[y,x],[x,x]]])

#polygon for ireland in  l1
#w.poly(parts = [[[-10,51],[-6,51],[-6,53.5],[-5.5,54],[-7,55.5],[-10,55.5],[-10,51]]])
#polygon for l4
#w.poly(parts = [[[-95,45],[-80,45],[-80,60],[-95,60],[-95,45]]])
#w.poly(parts = [[[-10,50], [-6,48], [3,48 ], [3,54], [-1,60],[-8,60],[-10,55], [-10,50]]])
"""
w.poly(parts= [[[4,0],[3,1],[4,2],[4,0]]])
w.field('1_FLD','C','40')
w.poly(parts=[ [[0,0],[1,1],[2,0],[0,0]]])
w.field('2_FLD','C','40')
w.poly(parts= [[[2,4],[3,3],[4,4],[2,4]]])
w.field('3_FLD','C','40')
w.poly(parts= [[[0,2],[1,3],[0,4],[0,2]]])
w.field('4_FLD','C','40')
w.poly(parts= [[[2,2],[3,1],[4,2],[2,2]]])
w.field('5_FLD','C','40')
w.poly(parts= [[[2,0],[3,1],[2,2],[2,0]]])
w.field('6_FLD','C','40')
w.poly(parts= [[[2,2],[3,3],[4,2],[2,2]]])
w.field('7_FLD','C','40')
w.poly(parts= [[[2,0],[1,1],[2,2],[2,0]]])
w.field('8_FLD','C','40')
w.poly(parts= [[[2,2],[3,3],[2,4],[2,2]]])
w.field('9_FLD','C','40')
w.poly(parts= [[[0,2],[1,1],[2,2],[0,2]]])
w.field('10_FLD','C','40')
w.poly(parts= [[[0,2],[1,3],[2,2],[0,2]]])
w.field('11_FLD','C','40')
w.poly(parts= [[[2,2],[1,3],[2,4],[2,2]]])
w.field('12_FLD','C','40')
w.poly(parts= [[[0,0],[1,1],[0,2],[0,0]]])
w.field('13_FLD','C','40')
w.poly(parts= [[[2,0],[3,1],[4,0],[2,0]]])
w.field('14_FLD','C','40')
w.poly(parts= [[[0,4],[1,3],[2,4],[0,4]]])
w.field('15_FLD','C','40')
"""
#w.poly(parts= [[[-100,-100],[100,300],[200,400],[-100,-100]]])
#w.field('16_FLD','C','40')


#w.poly(shapeType=5, parts =[[ [0,3,6,9,12,15,18,21,24,27,30,33,36,39,42]]])	
#print(w.shapes[0].parts)
w.poly(shapeType=5,parts=[[[4,0],[3,1],[4,2],[4,0],[0,0],[1,1],[2,0],[0,0],[2,4],[3,3],[4,4],[2,4],[0,2],[1,3],[0,4],[0,2],[2,2],[3,1],[4,2],[2,2],[2,0],[3,1],[2,2],[2,0],[2,2],[3,3],[4,2],[2,2],[2,0],[1,1],[2,2],[2,0],[2,2],[3,3],[2,4],[2,2],[0,2],[1,1],[2,2],[0,2],[0,2],[1,3],[2,2],[0,2],[2,2],[1,3],[2,4],[2,2],[0,0],[1,1],[0,2],[0,0],[2,0],[3,1],[4,0],[2,0],[0,4],[1,3],[2,4],[0,4],[4,2],[3,3],[4,4],[4,2]]])
w.field('Shape','C','40')
#w.save("testM")

w.record('First','Polygon')
w.save('p')
