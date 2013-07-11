# Take in the shapefile given and convert to .geo file.

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
