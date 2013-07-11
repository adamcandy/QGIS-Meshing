from shapely.ops import cascaded_union
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
