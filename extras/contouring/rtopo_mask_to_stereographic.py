#!/usr/bin/env python

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

import sys
import shutil
import math

from Scientific.IO import NetCDF
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot
from pylab import contour
#import matplotlib
#matplotlib._cntr.Cntr
#from matplotlib import contour
#matplotlib.use('Agg')
from numpy import zeros, array, append, exp
import gmsh

#contour = matplotlib.pyplot.contour

# TODO
# Calculate area in right projection
# Add region selection function
# Ensure all islands selected
# Identify Open boundaries differently
# Export command line to geo file
# If nearby, down't clode with parallel

def printv(text):
  if (arguments.verbose):
    print text
  gmsh.gmsh_geo_comment(output, text)

def printvv(text):
  if (arguments.debug):
    print text

def expand_boxes(region, boxes):
  def error():
    print 'Error in argument for -b.'
    sys.exit(1)

  def build_function(function, requireand, axis, comparison, number):
    if (len(number) > 0):
      function = '%s%s(%s %s %s)' % (function, requireand, axis, comparison, number)
      requireand = ' and '
    return [function, requireand]

  #re.sub(pattern, repl, string,
  #((latitude >= -89.0) and (latitude <=-65.0) and (longitude >= -64.0) and (longitude <= -20.0))'
  if (len(boxes) > 0):
    function = ''
    requireor = ''
    for box in boxes:
      longlat = box.split(',')
      if (len(longlat) != 2): error()

      long = longlat[0].split(':')
      lat = longlat[1].split(':')
      if ((len(long) != 2) and (len(lat) != 2)): error()
      
      function_box = ''
      requireand = ''
      if (len(long) == 2):
        [function_box, requireand] = build_function(function_box, requireand, 'longitude', '>=', long[0])
        [function_box, requireand] = build_function(function_box, requireand, 'longitude', '<=', long[1])
      if (len(lat) == 2):
        [function_box, requireand] = build_function(function_box, requireand, 'latitude',  '>=', lat[0])
        [function_box, requireand] = build_function(function_box, requireand, 'latitude',  '<=', lat[1])

      if (len(function_box) > 0):
        function = '%s%s(%s)' % (function, requireor, function_box)
        requireor = ' or '
  
    if (len(function) > 0):
      if (region is not 'True'):
        region = '((%s) and (%s))' % (region, function)
      else:
        region = function

  return region

def usage():
  print '''
 -n filename                 | Input netCDF file
 -f filename                 | Output Gmsh file
 -p path1 (path2)..          | Specify paths to include
 -r function                 | Function specifying region of interest
 -b box1 (box2)..            | Boxes with regions of interest
 -a minarea                  | Minimum area of islands
 -dx dist                    | Distance of steps when drawing parallels and meridians (currently in degrees - need to project)
 -bounding_latitude latitude | Latitude of boundary to close the domain
 -bl latitude                | Short form of -bounding_latitude
 -exclude_iceshelves         | Excludes iceshelf ocean cavities from mesh (default behaviour includes region)
 -smooth_data degree         | Smoothes boundaries
 -no                         | Do not include open boundaries
 -lat latitude               | Latitude to extent open domain to
 -s scenario                 | Select scenario (in development)
 -v                          | Verbose
 -vv                         | Very verbose (debugging)
 -q                          | Quiet
 -h                          | Help
------------------------------------------------------------
Example usage:
Include only the main Antarctic mass (path 1), and only parts which lie below 60S
  ./rtopo_mask_to_stereographic.py RTopo105b_50S.nc -r 'latitude <= -60.0' -p 1
Filchner-Ronne extended out to the 65S parallel
  ./rtopo_mask_to_stereographic.py RTopo105b_50S.nc -no -b -85.0:-20.0,-89.0:-75.0 -64.0:-30.0,-89.0:-70.0 -30.0:-20.0,-89.0:-75.0 -lat '-65.0'
Antarctica, everything below the 60S parallel, coarse approximation to open boundary
  ./rtopo_mask_to_stereographic.py RTopo105b_50S.nc -dx 2 -r 'latitude <= -60'
Small region close to the Filcher-Ronne ice shelf
  ./rtopo_mask_to_stereographic.py RTopo105b_50S.nc -no -b -85.0:-20.0,-89.0:-75.0 -64.0:-30.0,-89.0:-70.0 -30.0:-20.0,-89.0:-75.0 -p 1 -r 'latitude <= -83'
Amundsen Sea
  ./rtopo_mask_to_stereographic.py RTopo105b_50S.nc -no -b -130.0:-85.0,-85.0:-60.0 -lat -64.0

Small islands, single out, or group with -p
  312, 314
  79 - an island on 90W 68S
'''
  sys.exit(0)

#def scenario(name):
#  filcher_ronne = argument

argv = sys.argv[1:]
dx_default = 0.1
class arguments:
  input  = './RTopo105b_50S.nc'
  #output = './stereographic_projection.geo'
  output = './shorelines.geo'
  boundaries = []
  region = 'True'
  box = []
  minarea = 0
  dx = dx_default
  extendtolatitude = None
  open = True
  verbose = True
  debug = False
  call = ' '.join(argv)
  bounding_lat = -50.0
  smooth_data = False
  smooth_degree = 100
  include_iceshelf_ocean_cavities = True

while (len(argv) > 0):
  argument = argv.pop(0).rstrip()
  if   (argument == '-h'): usage()
  elif (argument == '-s'): arguments.scenario = str(argv.pop(0).rstrip()); arguments=scenario(arguments.scenario)
  elif (argument == '-n'): arguments.input  = argv.pop(0).rstrip()
  elif (argument == '-f'): arguments.output = argv.pop(0).rstrip()
  elif (argument == '-r'): arguments.region = argv.pop(0).rstrip()
  elif (argument == '-dx'): arguments.dx = float(argv.pop(0).rstrip())
  elif (argument == '-lat'): arguments.extendtolatitude = float(argv.pop(0).rstrip())
  elif (argument == '-a'): arguments.minarea = float(argv.pop(0).rstrip())
  elif (argument == '-bounding_latitude'): arguments.bounding_lat =float(argv.pop(0).rstrip())
  elif (argument == '-bl'): arguments.bounding_lat = float(argv.pop(0).rstrip())
  elif (argument == '-smooth_data'):
    arguments.smooth_degree = int(argv.pop(0).rstrip())
    arguments.smooth_data = True
  elif (argument == '-no'): arguments.open = False
  elif (argument == '-exclude_ice_shelves'): arguments.include_iceshelf_ocean_cavities = False
  elif (argument == '-v'): arguments.verbose = True
  elif (argument == '-vv'): arguments.verbose = True; arguments.debug = True; 
  elif (argument == '-q'): arguments.verbose = False
  elif (argument == '-p'):
    while ((len(argv) > 0) and (argv[0][0] != '-')):
      arguments.boundaries.append(int(argv.pop(0).rstrip()))
  elif (argument == '-b'):
    while ((len(argv) > 0) and ((argv[0][0] != '-') or ( (argv[0][0] == '-') and (argv[0][1].isdigit()) ))):
      arguments.box.append(argv.pop(0).rstrip())

arguments.region = expand_boxes(arguments.region, arguments.box)
 

source = file(arguments.input,'r')
output = file(arguments.output,'w')

gmsh.gmsh_geo_comment(output, 'Arguments: ' + arguments.call)
printv('Source netCDF located at ' + arguments.input)
printv('Output to ' + arguments.output)
if (len(arguments.boundaries) > 0):
  printv('Boundaries restricted to ' + str(arguments.boundaries))
if (arguments.region is not 'True'):
  printv('Region defined by ' + str(arguments.region))
if (arguments.dx != dx_default):
  printv('Open contours closed with a line formed by points spaced %g degrees apart' % (arguments.dx))
if (arguments.extendtolatitude is not None):
  printv('Extending region to meet parallel on latitude ' + str(arguments.extendtolatitude))

gmsh.gmsh_geo_comment(output, '')

def smoothGaussian(list,degree,strippedXs=False):
  list = list.tolist()
  window=degree*2-1
  weight=array([1.0]*window)
  weightGauss=[]
  for i in range(window):
    i=i-degree+1
    frac=i/float(window)
    gauss=1/(exp((4*(frac))**2))
    weightGauss.append(gauss)
  weight=array(weightGauss)*weight
  smoothed=[0.0]*(len(list)-window)
  for i in range(len(smoothed)):
    smoothed[i]=sum(array(list[i:i+window])*weight)/sum(weight)
  return array(smoothed)

def project(location):
  longitude = location[0]
  latitude  = location[1]
  cos = math.cos
  sin = math.sin
  #pi  = math.pi
  #longitude_rad2 = longitude * ( pi / 180 )
  #latitude_rad2  = latitude  * ( pi / 180 )
  longitude_rad = math.radians(- longitude - 90)
  latitude_rad  = math.radians(latitude)
  # Changed sign in x formulae - need to check
  x = sin( longitude_rad ) * cos( latitude_rad ) / ( 1 + sin( latitude_rad ) );
  y = cos( longitude_rad ) * cos( latitude_rad  ) / ( 1 + sin( latitude_rad ) );
  return [ x, y ]

def read_rtopo(filename):
  file = NetCDF.NetCDFFile(filename, 'r')
  #variableNames = fileN.variables.keys() 
  lon = file.variables['lon'][:] 
  lat = file.variables['lat'][:] 
  field = file.variables['z'][:, :] 
  #             % 2
  # 0 ocean    1
  # 1 ice      0
  # 2 shelf    1
  # 3 rock     0
  if arguments.include_iceshelf_ocean_cavities == True:
    printv('Including iceshelf ocean cavities')
    field = field % 2
  else:
    printv('Excluding iceshelf ocean cavities')
    field[field>0.5]=1 
  paths = contour(lon,lat,field,levels=[0.5]).collections[0].get_paths()
  return paths

def area_enclosed(p):
  return 0.5 * abs(sum(x0*y1 - x1*y0 for ((x0, y0), (x1, y1)) in segments(p)))

def segments(p):
  return zip(p, p[1:] + [p[0]])

def check_point_required(region, location):
  # make all definitions of the math module available to the function
  globals=math.__dict__
  globals['longitude'] = location[0]
  globals['latitude']  = location[1]
  return eval(region, globals)

def array_to_gmsh_points(num, index, location, minarea, region, dx, latitude_max):
  gmsh.gmsh_geo_comment(output, 'Ice-Land mass number %s' % (num))
  count = 0 
  pointnumber = len(location[:,0])
  valid = [False]*pointnumber
  validnumber = 0

  loopstart = None
  loopend = None
  flag = 0
  #location[:, 0] = - location[:, 0] - 90.0
  for point in range(pointnumber):
    longitude = location[point, 0]
    latitude  = location[point, 1]
    if ( check_point_required(region, location[point, :]) ):
      valid[point] = True
      validnumber += 1
      if (flag == 0):
        loopstart = point
        flag = 1
      elif (flag == 1):
        loopend = point
    #print latitude, valid[point]
    
  if (loopend is None):
    printvv('Path %i skipped (no points found in region)' % ( num ))
    gmsh.gmsh_geo_comment(output, '  Skipped (no points found in region)\n')
    return index
  
  closelast=False
  if (compare_points(location[loopstart,:], location[loopend,:], dx)):
    # Remove duplicate line at end
    # Note loopend no longer valid
    valid[loopend] = False
    validnumber -= 1
    closelast=True

  validlocation = zeros( (validnumber, 2) )
  close = [False]*validnumber
  count = 0
  closingrequired = False
  closingrequirednumber = 0
  for point in range(pointnumber):
    if (valid[point]):
      validlocation[count,:] = location[point,:]
      if ((closingrequired) and (count > 0)):
        if (compare_points(validlocation[count-1,:], validlocation[count,:], dx)):
          closingrequired = False
      close[count] = closingrequired
      count += 1
      closingrequired = False
    else:
      if (not closingrequired):
        closingrequired = True
        closingrequirednumber += 1

  if (closelast):
    close[-1] = True
    closingrequirednumber += 1
    

  if (closingrequirednumber == 0): 
    closingtext = ''
  elif (closingrequirednumber == 1): 
    closingtext = ' (required closing in %i part of the path)' % (closingrequirednumber)
  else:
    closingtext = ' (required closing in %i parts of the path)' % (closingrequirednumber)
      
  area = area_enclosed(validlocation)
  if (area < minarea):
    printvv('Path %i skipped (area too small)' % ( num ))
    gmsh.gmsh_geo_comment(output, '  Skipped (area too small)\n')
    return index

  printv('Path %i points %i/%i area %g%s' % ( num, validnumber, pointnumber, area_enclosed(validlocation), closingtext ))
 
  # if (closingrequired and closewithparallel):
  #   latitude_max = None
  #   index_start = index + 1
  #   for point in range(validnumber - 1):
  #     longitude = validlocation[point,0]
  #     latitude  = validlocation[point,1]
  #     index += 1
  #     loc = project(longitude, latitude)
  #     gmsh.gmsh_geo_draw_point(output, index, loc, 0) )
  #     if (latitude_max is None):
  #       latitude_max = latitude
  #     else:
  #       latitude_max = max(latitude_max, latitude)
  #   gmsh.gmsh_geo_draw_parallel(output, index, index_start, [ validlocation[point,0], max(latitude_max, validlocation[point,1]) ], [ validlocation[0,0], max(latitude_max, validlocation[0,1]) ], points=200)
  #   index += 200
  #   
  #   index += 1
  #   gmsh.gmsh_geo_draw_point(output, index, project(validlocation[0,0], validlocation[0,1]), 0) )
  #   
  # else:
  if (close[0]):
    close[-1] = close[0]
  
  index.start = index.point + 1
  loopstartpoint = index.start
  for point in range(validnumber):
    #longitude = validlocation[point,0]
    #latitude  = validlocation[point,1]
    
    if ((close[point]) and (point == validnumber - 1) and (not (compare_points(validlocation[point], validlocation[0], dx)))):
      gmsh.gmsh_geo_comment(output, '**** END ' + str(point) + '/' + str(validnumber-1) + str(close[point]))
      index = gmsh.gmsh_geo_draw_loop(output, boundary, index, loopstartpoint, False, False)
      index = draw_parallel_explicit(validlocation[point], validlocation[0], index, latitude_max, dx)
      index = gmsh.gmsh_geo_draw_loop(output, boundary, index, loopstartpoint, True, True)
      gmsh.gmsh_geo_comment(output, '**** END end of loop ' + str(closelast) + str(point) + '/' + str(validnumber-1) + str(close[point]))
    elif ((close[point]) and (point > 0) and (not (compare_points(validlocation[point], validlocation[0], dx)))):
      gmsh.gmsh_geo_comment(output, '**** NOT END ' + str(point) + '/' + str(validnumber-1) + str(close[point]))
      gmsh.gmsh_geo_comment(output, str(validlocation[point,:]) + str(validlocation[point,:]))
      index = gmsh.gmsh_geo_draw_loop(output, boundary, index, loopstartpoint, False, False)
      index = draw_parallel_explicit(validlocation[point - 1], validlocation[point], index, latitude_max, dx)
      index = gmsh.gmsh_geo_draw_loop(output, boundary, index, loopstartpoint, False, True)
      gmsh.gmsh_geo_comment(output, '**** NOT END end of loop ' + str(point) + '/' + str(validnumber-1) + str(close[point]))
    else:
      index.point += 1
      gmsh.gmsh_geo_draw_point(output, index.point, project(validlocation[point,:]), 0)
      index.contournodes.append(index.point)

  index = gmsh.gmsh_geo_draw_loop(output, boundary, index, loopstartpoint, (closelast and (point == validnumber - 1)), False)

  return index

#LoopStart1 = IP + 20;
#LoopEnd1 = IP + 3157;
#BSpline ( IL + 1 ) = { IP + 20 : IP + 3157 };
#Line Loop( ILL + 10 ) = { IL + 1 };
#
#LoopStart1 = IP + 3157;
#LoopEnd1 = IP + 3231;
#BSpline ( IL + 2 ) = { IP + 3157 : IP + 3231, IP + 20 };
#Line Loop( ILL + 20 ) = { IL + 2 };


def output_boundaries(index, filename, paths=None, minarea=0, region='True', dx=0.1, latitude_max=None):
  pathall = read_rtopo(filename)
  printv('Paths found: ' + str(len(pathall)))
  gmsh.gmsh_geo_header(output)
  splinenumber = 0
  indexbase = 1
  index.point = indexbase

  if ((paths is not None) and (len(paths) > 0)):
    pathids=paths
  else:
    pathids=range(len(pathall)+1)[1:]

  for num in pathids:
    xy=pathall[num-1].vertices
    if arguments.smooth_data:
      x = smoothGaussian(xy[:,0], degree=arguments.smooth_degree)
      y = smoothGaussian(xy[:,1], degree=arguments.smooth_degree)
      xy = zeros([len(x),2])
      xy[:,0] = x
      xy[:,1] = y
    index = array_to_gmsh_points(num, index, xy, minarea, region, dx, latitude_max)
  #for i in range(-85, 0, 5):
  #  indexend += 1
  #  gmsh.gmsh_geo_draw_point(output, indexend, project(0, i), 0) )
  #for i in range(-85, 0, 5):
  #  indexend += 1
  #  gmsh.gmsh_geo_draw_point(output, indexend, project(45, i), 0) )
  gmsh.gmsh_geo_remove_projection_points(output)
  return index

def compare_points(a, b, dx):
  tolerance = dx * 0.6
  if ( not (abs(a[1] - b[1]) < tolerance) ):
    #gmsh.gmsh_geo_comment(output, 'lat differ')
    return False
  elif (abs(a[0] - b[0]) < tolerance):
    #gmsh.gmsh_geo_comment(output, 'long same')
    return True
  elif ((abs(abs(a[0]) - 180) < tolerance) and (abs(abs(b[0]) - 180) < tolerance)):
    #gmsh.gmsh_geo_comment(output, 'long +/-180')
    return True
  else:
    #gmsh.gmsh_geo_comment(output, 'not same %g %g' % (abs(abs(a[0]) - 180), abs(abs(b[0]) - 180) ) )
    return False


def output_open_boundaries(index, boundary, dx):
  parallel = arguments.bounding_lat
  index.start = index.point + 1
  loopstartpoint = index.start
  index = draw_parallel_explicit([   -1.0, parallel], [ 179.0, parallel], index, None, dx)
  index = draw_parallel_explicit([-179.0,  parallel], [   1.0, parallel], index, None, dx)
  
  index = gmsh.gmsh_geo_draw_loop(output, boundary, index, loopstartpoint, True, True)

  return index


def draw_parallel_explicit(start, end, index, latitude_max, dx):

  #print start, end, index.point
  # Note start is actual start - 1
  if (latitude_max is None):
    latitude_max = max(start[1], end[1])
  else:
    latitude_max = max(latitude_max, start[1], end[1])
  current = start
  tolerance = dx * 0.6

  gmsh.gmsh_geo_comment(output, 'Closing path with parallels and merdians, from (%.8f, %.8f) to  (%.8f, %.8f)' % ( start[0], start[1], end[0], end[1] ) )

  if (compare_points(current, end, dx)):
    gmsh.gmsh_geo_comment(output, 'Points already close enough, no need to draw parallels and meridians after all')
    return index

  gmsh.gmsh_geo_comment(output, 'Drawing meridian to max latitude index %s at %f.2, %f.2 (to match %f.2)' % (index.point, current[0], current[1], latitude_max))
  while (current[1] != latitude_max):
    if (current[1] < latitude_max):
      current[1] = current[1] + dx
    else:
      current[1] = current[1] - dx
    if (abs(current[1] - latitude_max) < tolerance): current[1] = latitude_max
    if (compare_points(current, end, dx)): return index
    index.point += 1
    printvv('Drawing meridian to max latitude index %s at %f.2, %f.2 (to match %f.2)' % (index.point, current[0], current[1], latitude_max))
    loc = project(current)
    gmsh.gmsh_geo_draw_point(output, index.point, loc, 0.0)

  gmsh.gmsh_geo_comment(output, 'Drawing parallel index %s at %f.2 (to match %f.2), %f.2' % (index.point, current[0], end[0], current[1]))
  while (current[0] != end[0]):
    if (current[0] < end[0]):
      current[0] = current[0] + dx
    else:
      current[0] = current[0] - dx
    if (abs(current[0] - end[0]) < tolerance): current[0] = end[0]
    if (compare_points(current, end, dx)): return index
    index.point += 1
    printvv('Drawing parallel index %s at %f.2 (to match %f.2), %f.2' % (index.point, current[0], end[0], current[1]))
    loc = project(current)
    gmsh.gmsh_geo_draw_point(output, index.point, loc, 0.0)

  gmsh.gmsh_geo_comment(output, 'Drawing meridian to end index %s at %f.2, %f.2 (to match %f.2)' % (index.point, current[0], current[1], end[1]))
  while (current[1] != end[1]):
    if (current[1] < end[1]):
      current[1] = current[1] + dx
    else:
      current[1] = current[1] - dx
    if (abs(current[1] - end[1]) < tolerance): current[1] = end[1]
    if (compare_points(current, end, dx)): return index
    index.point += 1
    printvv('Drawing meridian to end index %s at %f.2, %f.2 (to match %f.2)' % (index.point, current[0], current[1], end[1]))
    loc = project(current)
    gmsh.gmsh_geo_draw_point(output, index.point, loc, 0.0)

  gmsh.gmsh_geo_comment(output, 'Closed path with parallels and merdians, from (%.8f, %.8f) to  (%.8f, %.8f)' % ( start[0], start[1], end[0], end[1] ) )

  return index


def acc_array():
  acc = array([[   1.0, -53.0 ],
[  10.0, -53.0 ],
[  20.0, -52.0 ],
[  30.0, -56.0 ],
[  40.0, -60.0 ],
[  50.0, -63.0 ],
[  60.0, -64.0 ],
[  70.0, -65.0 ],
[  80.0, -67.0 ],
[  90.0, -60.0 ],
[ 100.0, -58.0 ],
[ 110.0, -62.0 ],
[ 120.0, -63.0 ],
[ 130.0, -65.0 ],
[ 140.0, -65.0 ],
[ 150.0, -64.0 ],
[ 160.0, -61.0 ],
[ 170.0, -64.0 ],
[ 179.0, -65.0 ],
[-179.0, -65.0 ],
[-170.0, -64.0 ],
[-160.0, -62.0 ],
[-150.0, -66.0 ],
[-140.0, -58.0 ],
[-130.0, -60.0 ],
[-120.0, -65.0 ],
[-110.0, -66.0 ],
[-100.0, -70.0 ],
[ -90.0, -70.0 ],
[ -80.0, -77.0 ],
[ -70.0, -72.0 ],
[ -60.0, -60.0 ],
[ -50.0, -57.0 ],
[ -40.0, -51.0 ],
[ -30.0, -50.0 ],
[ -20.0, -60.0 ],
[ -10.0, -56.0 ],
[ -1.0, -53.0 ]])
  return acc


def draw_acc_old(index, boundary, dx):
  acc = acc_array()
  gmsh.gmsh_geo_comment(output, 'ACC')
  index.start = index.point + 1
  loopstartpoint = index.start
  for i in range(len(acc[:,0])):
    index.point += 1
    location = project(acc[i,:])
    gmsh.gmsh_geo_draw_point(output, index.point, location, 0.0)

  for i in range(len(acc[:,0])):
    a = index.start + i
    b = a + 1
    if (a == index.point):
      b = index.start
    output.write('Line(%i) = {%i,%i};\n' % (i + 100000, a, b  ))
  output.write('Line Loop(999999) = { %i : %i};\n' % ( index.start, index.point ))
  return index


def draw_acc(index, boundary, dx):
  acc = acc_array()
  acc1 = acc[0:18,:]
  acc2 = acc[19:,:]
  print acc1
  print acc2
  gmsh.gmsh_geo_comment(output, 'ACC')

  index.start = index.point + 1
  loopstartpoint = index.start
  for i in range(len(acc1[:,0])):
    index.point += 1
    location = project(acc1[i,:])
    gmsh.gmsh_geo_draw_point(output, index.point, location, 0.0)
  index = gmsh.gmsh_geo_draw_loop(output, boundary, index, loopstartpoint, False, True)

  #index.start = index.point + 1
  #loopstartpoint = index.start
  for i in range(len(acc2[:,0])):
    index.point += 1
    location = project(acc2[i,:])
    gmsh.gmsh_geo_draw_point(output, index.point, location, 0.0)
  index = gmsh.gmsh_geo_draw_loop(output, boundary, index, loopstartpoint, True, True)

  return index


class index:
  point = 0
  path = 0
  contour = []
  contournodes= []
  open = []
  skipped = []
  start = 0
  pathsinloop = []
  loop = 0
  loops = []

class boundary:
  contour = 3
  open    = 4
  surface = 9


index = output_boundaries(index, filename=arguments.input, paths=arguments.boundaries, minarea=arguments.minarea, region=arguments.region, dx=arguments.dx, latitude_max=arguments.extendtolatitude)


if (arguments.open): index = output_open_boundaries(index, boundary, arguments.dx)
printv('Open boundaries   (id %i): %s' % (boundary.open, gmsh.list_to_space_separated(index.open, add=1)))
printv('Closed boundaries (id %i): %s' % (boundary.contour, gmsh.list_to_space_separated(index.contour, add=1)))
gmsh.gmsh_geo_define_surfaces(output, index, boundary)

#index = draw_acc(index, boundary, arguments.dx)


gmsh.gmsh_geo_output_fields(output, index,boundary)


if (len(index.skipped) > 0):
  printv('Skipped (because no point on the boundary appeared in the required region, or area enclosed by the boundary was too small):\n'+' '.join(index.skipped))
output.close()
