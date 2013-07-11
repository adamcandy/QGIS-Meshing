#imports the library shapefile to allow the shapefile operations
import shapefile

readPath = "p.shp"
writePath = "w.shp"




line = "Point(2) = {1,2,3,4}"

tokens = parsePoint(line)

for t in tokens:
	print t + " "


"""
read = open(readPath,"r")
write = shapefile.Editor(shapefile=writePath) 

while 1 : 


	line = f.readline()
	if not line :
		print 'end of file'
		break
	points = parsePoint(line)
	writePointToFile(points,write)

	print 'written to file  --> '
	print line

read.close()
write.close()

"""

def writePointToFile(points,fileStream):
	f = shapefile.Editor(shapefile=fp)
	fileStream.point(float(points[0]),float(points[1]),float(points[2]),float(points[3]))
	fileStream.record("Appended","Point")
	fileStream.save(fp)
	return


def parsePoint(line):
	if 'Point' in line :
		tokens = line.split('= {',2)
	  points = tokens[1].split(', ',4)
		points[3] = points[3][0:len(points[3])-3]
		return points
