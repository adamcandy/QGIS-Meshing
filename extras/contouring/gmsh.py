

##########################################################################
#  
#  Generation of boundary representation from arbitrary geophysical
#  fields and initialisation for anisotropic, unstructured meshing.
#  
#  Copyright (C) 2011-2013 Dr Adam S. Candy, adam.candy@imperial.ac.uk
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  
##########################################################################

def gmsh_geo_header(output):
  '''Function writing the header to the Gmsh .geo file. The header consits of creation
     of new IDs for point, line, line-loops, surface and field entities. Then the first
     point is drawn on the centre of the planet and the second point is drawn on the North
     pole. The last statement in the header instructs Gmsh that the following geometry
     commands are on the strereographic projection plane. Note that the planet is
     modelled as a sphere.'''
  earth_radius = 6.37101e+06
  output.write( '''
IP = newp;
IL = newl;
ILL = newll;
IS = news;
IFI = newf;
Point ( IP + 0 ) = { 0, 0, 0 };
Point ( IP + 1 ) = { 0, 0, %(earth_radius)g };
PolarSphere ( IS + 0 ) = { IP, IP + 1 };

''' % { 'earth_radius': earth_radius } )


def gmsh_geo_footer(output, loopstart, loopend):
  output.write( '''
Field [ IFI + 0 ]  = Attractor;
Field [ IFI + 0 ].NodesList  = { IP + %(loopstart)i : IP + %(loopend)i };
''' % { 'loopstart':loopstart, 'loopend':loopend } )

def gmsh_geo_remove_projection_points(output):
  '''Function deleting the points placed at the centre of the geoid and at the north pole.'''
  output.write( '''
Delete { Point{1}; }
Delete { Point{2}; }
''' )


def gmsh_geo_comment(output, comment):
  '''Function witing a single-line comment to Gmsh geo script file.'''
  output.write( '// ' + comment + '\n')


def gmsh_geo_draw_point(output, index, loc, z):
  '''Function writing (drawing) a point to the Gmsh geo script file.'''
  accuracy = '.8'
  format = 'Point ( IP + %%i ) = { %%%(dp)sf, %%%(dp)sf, %%%(dp)sf };\n' % { 'dp': accuracy }
  output.write(format % (index, loc[0], loc[1], z))


def gmsh_geo_draw_loop(output, boundary, index, loopstartpoint, last, open):
  '''Function writing (drawing) a line-loop to the Gmsh geo script file.'''
  if (index.point <= index.start):
    return index
  #pointstart = indexstart
  #pointend   = index.point
  #loopnumber = index.loop
  if (last):
    closure = ', IP + %(pointstart)i' % { 'pointstart':loopstartpoint }
  else:
    closure = ''
  if (open):
    index.open.append(index.path)
    boundaryid = boundary.open
    type = 'open'
  else:
    index.contour.append(index.path)
    type = 'contour'
    boundaryid = boundary.contour

  index.pathsinloop.append(index.path)

#//Line Loop( ILL + %(loopnumber)i ) = { IL + %(loopnumber)i };
#// Identified as a %(type)s path

  output.write( '''LoopStart%(loopnumber)i = IP + %(pointstart)i;
LoopEnd%(loopnumber)i = IP + %(pointend)i;
BSpline ( IL + %(loopnumber)i ) = { IP + %(pointstart)i : IP + %(pointend)i%(loopstartpoint)s };
Physical Line( %(boundaryid)i ) = { IL + %(loopnumber)i };

''' % { 'pointstart':index.start, 'pointend':index.point, 'loopnumber':index.path, 'loopstartpoint':closure, 'type':type, 'boundaryid':boundaryid } )

  if (last):
    output.write( '''Line Loop( ILL + %(loop)i ) = { %(loopnumbers)s };
''' % { 'loop':index.loop , 'loopnumbers':list_to_comma_separated(index.pathsinloop, prefix = 'IL + ') } )
    index.loops.append(index.loop)
    index.loop += 1
    index.pathsinloop = []

  index.path +=1
  index.start = index.point
  return index


def gmsh_geo_define_point(output, name, location):
  '''Function writing a point definition in longitude-latitude as wall as in cartesian
     coordinates in the stereographic projection plane. No points are drawn in Gmsh,
     variables are assigned'''
  # location [long, lat]
  output.write('''
//Point %(name)s is located at, %(longitude).2f deg, %(latitude).2f deg.
Point_%(name)s_longitude_rad = (%(longitude)f + (00/60))*(Pi/180);
Point_%(name)s_latitude_rad  = (%(latitude)f + (00/60))*(Pi/180);
Point_%(name)s_stereographic_y = Cos(Point_%(name)s_longitude_rad)*Cos(Point_%(name)s_latitude_rad)  / ( 1 + Sin(Point_%(name)s_latitude_rad) );
Point_%(name)s_stereographic_x = Cos(Point_%(name)s_latitude_rad) *Sin(Point_%(name)s_longitude_rad) / ( 1 + Sin(Point_%(name)s_latitude_rad) );
''' % { 'name':name, 'longitude':location[0], 'latitude':location[1] } )


def gmsh_geo_draw_parallel(output, startn, endn, start, end, points=200):
  '''Function for drawing a parallel-segment through specified points.'''
  startp = project(start)
  endp = project(end)

  output.write('''
pointsOnParallel = %(points)i;
parallelSectionStartingX = %(start_x)g;
parallelSectionStartingY = %(start_y)g;
firstPointOnParallel = IP + %(start_n)i;
parallelSectionEndingX = %(end_x)g;
parallelSectionEndingY = %(end_y)g;
lastPointOnParallel = IP + %(end_n)i;
newParallelID = IL + 10100;
Call DrawParallel;
''' % { 'start_x':startp[0], 'start_y':startp[1], 'end_x':endp[0], 'end_y':endp[1], 'start_n':startn, 'end_n':endn, 'points':points })


def gmsh_geo_define_surfaces(output, index, boundary):
  '''Function declaring plane surfaces in gmsh geo script file.'''
  boundary_list = list_to_comma_separated(index.contour + index.open)
#//Line Loop( ILL + %(loopnumber)i ) = { %(boundary_list)s };
#//Plane Surface( %(surface)i ) = { ILL + %(loopnumber)i };
  output.write('''
Plane Surface( %(surface)i ) = { %(boundary_list)s };
Physical Surface( %(surface)i ) = { %(surface)i };
''' % { 'loopnumber':index.path, 'surface':boundary.surface + 1, 'boundary_list':list_to_comma_separated(index.loops, prefix = 'ILL + ') } )


def gmsh_geo_output_fields(output, index,boundary):
  '''Function writing fields controlling mesh size to gmsh geo file. This function also writes
     some other options to the geo file, an operation that should probably be performed somewhere else.'''
  if (index.contour is not None):
    output.write('''
Printf("Assigning characteristic mesh sizes...");
// Field[ IFI + 1] = Attractor;
// Field[ IFI + 1].EdgesList = { 999999, %(boundary_list)s };
// Field [ IFI + 1 ].NNodesByEdge = 5e4;
// 
// Field[ IFI + 2] = Threshold;
// Field[ IFI + 2].DistMax = 2e6;
// Field[ IFI + 2].DistMin = 3e4;
// Field[ IFI + 2].IField = IFI + 1;
// Field[ IFI + 2].LcMin = 5e4;
// Field[ IFI + 2].LcMax = 2e5;
//
// Background Field = IFI + 2;
// Dont extent the elements sizes from the boundary inside the domain
//Mesh.CharacteristicLengthExtendFromBoundary = 0;

Field[ IFI + 1] = MathEval;
Field[ IFI + 1].F = "1.0E5";
Background Field = IFI + 1;

//Set some options for better png output
General.Color.Background = {255,255,255};
General.Color.BackgroundGradient = {255,255,255};
General.Color.Foreground = Black;
Mesh.Color.Lines = {0,0,0};

General.Trackball = 0 ;
General.RotationX = 180;
General.RotationY = 0;
General.RotationZ = 270;
''' % { 'boundary_list':list_to_comma_separated(index.contour, prefix = 'IL + ') } )


def gmsh_geo_define_loop(output, index, loopstartpoint, last, open):
  '''Function writing line-loops to gmsh geo file.'''
  if (index.point <= index.start):
    return index
  #pointstart = indexstart
  #pointend   = index.point
  #loopnumber = index.loop
  if (last):
    closure = ', IP + %(pointstart)i' % { 'pointstart':loopstartpoint }
  else:
    closure = ''
  if (open):
    index.open.append(index.path)
    type = 'open'
  else:
    index.contour.append(index.path)
    type = 'contour'

  index.pathsinloop.append(index.path)

#//Line Loop( ILL + %(loopnumber)i ) = { IL + %(loopnumber)i };
#// Identified as a %(type)s path

  output.write( '''LoopStart%(loopnumber)i = IP + %(pointstart)i;
LoopEnd%(loopnumber)i = IP + %(pointend)i;
BSpline ( IL + %(loopnumber)i ) = { IP + %(pointstart)i : IP + %(pointend)i%(loopstartpoint)s };
Physical Line( IL + %(loopnumber)i ) = { IL + %(loopnumber)i };

''' % { 'pointstart':index.start, 'pointend':index.point, 'loopnumber':index.path, 'loopstartpoint':closure, 'type':type } )

  if (last):
    output.write( '''Line Loop( ILL + %(loop)i ) = { %(loopnumbers)s };
''' % { 'loop':index.loop , 'loopnumbers':list_to_comma_separated(index.pathsinloop, prefix = 'IL + ') } )
    index.loops.append(index.loop)
    index.loop += 1
    index.pathsinloop = []

  index.path +=1
  index.start = index.point
  return index

def list_to_comma_separated(numbers, prefix='', add=0):
  '''Function converting a python list to a comma-seperated string.'''
  requirecomma = False
  string = ''
  for number in numbers:
    if (requirecomma):
      string += ', '
    else:
      requirecomma = True
    string += prefix
    string += str(number + add)
  return string

def list_to_space_separated(numbers, prefix='', add=0):
  '''Function converting a python list to a space-separated string.'''
  requirespace = False
  string = ''
  for number in numbers:
    if (requirespace):
      string += ' '
    else:
      requirespace = True
    string += prefix
    string += str(number + add)
  return string
