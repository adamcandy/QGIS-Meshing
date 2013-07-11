import shapefile
from shapely.geometry import *
import sys
import matplotlib.pyplot as pyplot

#make a point shape file

#p1 = Point(0.5,0.5)

poly = Polygon([(0,0),(1,0),(1,1),(0,1),(0,0)])

#print(p1.within(poly))


#check if the number of command  line arguments are 
#ok

assert len(sys.argv)==4, "Incorrect Number of Arguments passed"


"""
Sets the read and the write file stream according to
the command line arguments given.

The first argument specifies which shape file the user
wants to specify the boundaries of

The second arguments specifies the boundary polygon

The third argument specifies the file path to which the
new shape has top be written

"""

readPath = sys.argv[1]
boundaryPath = sys.argv[2]
writePath = sys.argv[3]

#input stream for the given shape
sf = shapefile.Reader(readPath)

#input stream of the boundaries
bounds = shapefile.Reader(boundaryPath)

#checks that there shouldonly be one boudary
#assert len(bounds.shapes())==1, "More than one shape in the boundary. Currently only one shape can be specified as a boundary"

boundary = bounds.shapes()
#assert len(boundaries)==1 , "Invalid number of boundaries. Only one baoundary is allowed"

boundaryPoints = list(boundary.exterior.coords)
print("boundaryPoints len = %d" % len(boundaryPoints))

"""
	This function checks if the given point is on the boundary.
	@param point : specifies the point which has to be checked
	@param bouds : specifies all the bpundary objects
	@return			 : returns true iff the point in on the boundary lines
"""
def checkPointOnBoundary(point):
	if (point.x,point.y) in boundaryPoints:
		return True
	points = boundary.exterior.coords
	numberOfPoints = len(points)
	for i in range(numberOfPoints-1):
		line = LineString([(points[i][0],points[i][1]),(points[i+1][0], points[i+1][1])])
		if (line.contains(point)):
			return True
	return False

w = []
i = -1
c = 1
for shape in shapes:
	i += 1
	w.append(shapefile.Writer(shapefile.Polygon))
	for point in pointslist[i]:
		p = Point(point[0],point[1])
		if p.within(boundary) or checkPointOnBoundary(p):
			w[i].point(p.x,p.y)
			w[i].field('%d_FLD' % c)
		c +=1
		"""
		if len(w[i].shapes())>=2:
			w[i].save(writePath)
		"""

print("Number of shapes = %d \n\n" % len(w))
n = 0
for shape in w: 
	print("shape %d contains %d points" %(n+1, len(w[i].shapes())))
	n += 1

for wr in w:
	for s in wr.shapes():
		x=[];y=[]
		for p in s.points:
			print(p)
			x.append(p.x)
			y.append(p.y)
		pyplot(x,y)


pyplot.xlim(-5, 5)
pyplot.ylim(-5, 5)
pyplot.show()

