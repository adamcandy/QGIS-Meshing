import sys
import shapefile
import math

def usage():
	print "Usage:\n$ python <NAME OF SCRIPT> <PATH OF .shp> <PATH TO WRITE>"

def same_point(x1,y1,x2,y2):
  dist = math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
  return (dist<=0.000001)


def export(shp, geo):
   shpFile = shp 
   geoFile =  open(geo,"w")
   shapes =  shpFile.shapes()
   records = shpFile.records()
   geoFile.write("//Projection of a plane on a sphere:\n\n\n")
   geoFile.write("Point(1) = {0.0,0.0,0.0}; //The center of the sphere\n")
   geoFile.write("Point(2) = {0.0,0.0,6.37101e+06}; //The North Pole\n")
   geoFile.write("PolarSphere(1) = {1,2};\n")
   pId = 3
   lId = 3
   zCoord = 0
   meshSize = 2
   lLoop = 1
   phLine = []
   geoFile.write("zCoord = %f;\n" %zCoord)
   geoFile.write("meshSize = %f;\n" %meshSize)
   # First of all, we'll remove the duplicates
   for i in range(len(shapes)):
     for j in range(len(shapes[i].points)):
       longitude = shapes[i].points[j][0]
       latitude  = shapes[i].points[j][1]
       cos = math.cos
       sin = math.sin
       longitude_rad = math.radians(- longitude - 90)
       latitude_rad  = math.radians(latitude)
       x = sin( longitude_rad ) * cos( latitude_rad ) / ( 1 + sin( latitude_rad ) )
       y = cos( longitude_rad ) * cos( latitude_rad  ) / ( 1 + sin( latitude_rad ) )
       shapes[i].points[j][0] = x
       shapes[i].points[j][1] = y

   for i in range(len(shapes)):
     for j in range(len(shapes[i].points)-1):
       while j < len(shapes[i].points)-1 and same_point(shapes[i].points[j][0], shapes[i].points[j][1], shapes[i].points[j+1][0], shapes[i].points[j+1][1]):
         trash = shapes[i].points.pop(j+1)
     trash = shapes[i].points.pop()
   # This for-loop extracts all the points, one by one, and writes them as it goes along
   for i in range(len(shapes)):
     shape = shapes[i]
     init = pId
     for coord in shape.points:
      
       geoFile.write("Point(%d) = {%f, %f, zCoord};\n" %(pId, coord[0], coord[1]))
       pId+=1
       prevPoint = coord
     
   geoFile.write("\n")
   pId = 3
   geoFile.write('\n')
  
   for i in range(len(shapes)):
    shape = shapes[i]
    record = records[i]
    init = pId  
    for j in range(len(shape.points)):
     if records[i][1]=="Boundary" and (i+1>=len(shapes) or  records[i+1][1][0]=='I') and j == len(shape.points)-1:
      geoFile.write("BSpline(%d) = {%d, 3};\n\n" %(lId, pId))
      phLine.append((int(record[0]), lId))
      lId+=1
      pId+=1
      continue
     if j == len(shape.points)-1 and record[1][0]=='I':
      geoFile.write("BSpline(%d) = {%d, %d};\n\n" %(lId, pId, init))
     else:
      geoFile.write("BSpline(%d) = {%d, %d};\n" %(lId, pId, pId+1))
     phLine.append((int(record[0]), lId))
     lId+=1
     pId+=1 

   

   lId = 3
   ok = True
   # The boundary can be splitted into many different shapes. That's why, the first line loop will contain only the boundary, regardless of how many shape it may encapsulate.
   planeSurface= "Plane Surface(1)={1"
   geoFile.write("Line Loop(1)={")
   for i in range(len(shapes)):
    if records[i][1][0] == 'I':
     break
    shape = shapes[i]
    for j in range(len(shape.points)):
     if ok:
      geoFile.write("%d" %lId)
      ok = False;
     else:
      geoFile.write(", %d" %lId)
     lId+=1
   geoFile.write("};\n")
   lLoop = 1

   # After having written the boundary, the line loops for writing each individual shape follow. 
   for i in range(len(shapes)):
    if records[i][1][0] != 'I':
     continue
    shape = shapes[i]
    lLoop += 1
    geoFile.write("Line Loop(%d)={" %(lLoop))
    planeSurface += ", " + str(lLoop)
    for j in range(len(shape.points)):
      if j == len(shape.points)-1:
       geoFile.write("%d" %lId)
      else:
       geoFile.write("%d, " %lId)
      lId+=1
    geoFile.write("};\n") 
   planeSurface += "};\n"
   geoFile.write(planeSurface)
   #Puts ths ids in the file as physical lines.
   # How it works: Takes the first element's id, passes it into the file as the id of a physical line and loops through the entire array, searching for lines with the same id. The lines that are found are added to that specific physical line and are deleted from the phLine array. All this stops when phLine will be empty.
   pids = ""
   while len(phLine) > 0:  
    finalId = phLine[0][0] 
    ok = False
    geoFile.write("Physical Line(%d) = {" %finalId)
    i = 0 
    while i < len(phLine):
     if phLine[i][0] == finalId:
      if ok:
       pids+=", "
       geoFile.write(", ")
      ok = True
      pids+=str(phLine[i][1])
      geoFile.write(str(phLine[i][1]))
      phLine.remove(phLine[i])
      continue
     i+=1   
    geoFile.write("};\n")
    # In order to mesh, I defined a default plane surface which will hold all the line loops in the file.
   geoFile.write("Physical Surface(1)={1};\n")
   geoFile.write("Printf(\"Assigning characteristic mesh sizes...\");\n")
   geoFile.write("Field[1] = Attractor;\n")
   geoFile.write("Field[1].EdgesList = {%s};\n" %pids) #TODO:Modify
   geoFile.write("Field[1].NNodesByEdge = 50;\n")
   geoFile.write("Field[2] = Threshold;\n")
   geoFile.write("Field[2].DistMax = 50000;\n")
   geoFile.write("Field[2].DistMin = 500;\n")
   geoFile.write("Field[2].IField = 1;\n")
   geoFile.write("Field[2].LcMin = 5000;\n")
   geoFile.write("Field[2].LcMax = 50000;\n")
   geoFile.write("Background Field = 2;\n")
   geoFile.write("// Dont extent the elements sizes from the boundary inside the domain\n")
   geoFile.write("Mesh.CharacteristicLengthExtendFromBoundary = 0;\n")
   geoFile.write("//Set some options for better png output\n")
   geoFile.write("General.Color.Background = {255,255,255};\n")
   geoFile.write("General.Color.BackgroundGradient = {255,255,255};\n")
   geoFile.write("General.Color.Foreground = Black;\n")
   geoFile.write("Mesh.Color.Lines = {0,0,0}; \n")
   geoFile.close()

def main():
	if len(sys.argv)!=3:
		usage()
		sys.exit()
	inFile = sys.argv[1]
	outFile = sys.argv[2]
	shape1 = shapefile.Reader(inFile)
	export(shape1, outFile)

if __name__ == '__main__':
  main()



 
