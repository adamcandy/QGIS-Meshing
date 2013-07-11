import shapefile
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
