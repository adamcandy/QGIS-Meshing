
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

"""
This script writes the geo file. This script works with multiple domains and the surface id for that domain
is same as the id for the shape file in the shapefile. This script also respects the physical line id which 
is defined using define_id script.

This script has an option to allow the user to choose if BSpline or Line has to be used. Another option is
to enable compound lines.

"""

#might change to arrays, but extreamly quick anyway

#import for message box to display error
from PyQt4.QtGui import QMessageBox
import numpy as np
import numpy.lib.arraysetops as nset
import copy

def _flatten( l1temp ): #replace with _r_l_g
  l2temp = []
  for i in l1temp:
      l2temp += i
  return l2temp

#def _flatten_np( arr ):


#would have to pass arr1 in as a Globals, still might need to call additional vectorize?, could probably change syntax
class __recersive_list_gen:
  def __init__( self, arr1, index, iscon, Globals = None, brk = False):
    #note arr1 and index might not nessicarilly be convertable to a numpy array
    self.Globals = Globals
    self.index = index
    f = lambda k, isc, self = self: self._sub_gen(k, isc, brk)
    self.new_list = dict(enumerate(map(f,range(len(arr1)),map(lambda k, self = self:eval(iscon,locals(),globals()),range(len(arr1))))))
    map(lambda x, self = self: self._rem_emp(x,self.new_list),self.new_list.keys())
    
  def _sub_gen( self, k, iscon, brk):
    a = np.extract(iscon,self.index)
    if brk and a.size != 0:
      return np.array([a[0]])
    return a

  def _rem_emp( self, x, diction ):
    if diction[x].size == 0:
      del diction[x]

def _set_dict( diction ):#rewrite _r_l_g
  new_list = []
  for val in diction.values():
    if np.any(map(lambda x: np.all(val == x), new_list)):
      continue
    new_list += [val]
  return dict(enumerate(new_list)) 


def unzip( arr1, index = 0):
  return map(lambda x: x[index], arr1)
  
#def unzip_d( diction, index = 0):
  #return map(lambda x, x[index], diction.values())


"""
This funcion writes the physical surafces in the geo file. The id used for
the physical surface is the id from the shapefile which contains all the region
ids which distingueshes multiple domains
@param region_id_list    : specifies the ids of different surfaces in a list 
@param number_of_regions : specifies the number of different surfaces in the #pointless
                           given domain data
@param geoFile           : file stream for the geo file to write the surfaces
"""
def __write_physical_surface_list_obs(region_id_list,number_of_regions,geoFile) :#why two physical surface calls?
  #unique_list = set(region_id_list)
  physical_id_dict = {}
  for i in range(len(region_id_list)):
    if not region_id_list[i] in physical_id_dict.keys():
      physical_id_dict[region_id_list[i]] = [i+1]
      continue
    physical_id_dict[region_id_list[i]].append(i+1)
  for k in physical_id_dict.keys():
    geoFile.write("Physical Surface(%i) = {%s};\n" % (k,str(physical_id_dict[k])[1:-1]))
    
def __write_physical_surface_list( region_id_list, p_surface_dict, geoFile ):#printing blanks
  physical_id_dict = {}
  p_k = p_surface_dict.keys()
  for i in range(len(region_id_list)):
    if region_id_list[i] in physical_id_dict.keys():
      continue
    lst = []
    for p in p_k:
      if p[1] == region_id_list[i]:
        lst.append(p[0])
    physical_id_dict[region_id_list[i]] = lst  
  for k in physical_id_dict.keys():
    geoFile.write("Physical Surface(%i) = {%s};\n" % (k,str(physical_id_dict[k])[1:-1]))


"""
This method writes the physical line ids for individual lines in teh given domain data.
This method uses a helper method second which returns the second element in the tuple
@param lines_ids : list of tuples which consists of the id for the line and the physical
                   id for the line
@param geoFile   : file stream for the geo file to write the physical lines
"""
def __write_physical_lines_to_geo(lines_ids, geoFile):
  def second(a):
    return a[1]
                      
  line_numbers = lines_ids[0]
  unique_pid_list = set(map(second,lines_ids))
  physical_line_id_dict = {}
  for pid in unique_pid_list:
    physical_line_id_dict[pid] = []
  for line,pid in lines_ids:
    physical_line_id_dict[pid].append(line)
  for i in range(len(physical_line_id_dict.keys())):
    geoFile.write("Physical Line(%i) = {%s};\n" % (physical_line_id_dict.keys()[i],str(physical_line_id_dict.values()[i])[1:-1]))

"""
This method writes the physical line ids for individual compound lines in the 
given domain data.
@param lines_ids : list of tuples which consists of the id for the line and the physical
                   id for the line
@param geoFile   : file stream for the geo file to write the physical lines
"""
def __write_physical_compound_lines_to_geo(lines_ids, geoFile):
  for key in lines_ids.keys():
    geoFile.write("Physical Line(%i) = {%s};\n" % (key,str(lines_ids[key])[1:-1]))

def __write_compound_lines_as_physical( compound_line_dict, geoFile ):
  keys = compound_line_dict.keys()
  keys = np.array(keys).transpose()
  physical_line_dict = {}
  for k in range(keys[0].size):
    if keys[1][k] in physical_line_dict.keys():
      physical_line_dict[keys[1][k]].append(keys[0][k])
      continue
    physical_line_dict[keys[1][k]] = [keys[0][k]]
  for k in physical_line_dict.keys():
    geoFile.write("Physical Line(%i) = {%s};\n" % (k,str(physical_line_dict[k])[1:-1]))#physical Line Ids may be wrong
    
#still missing some compound lines in some instances, possibly working under the assumtion that the idpolygons only intersect the boundary once?
#optermising this code is vital it is the slowest part of the script
def __split_compound_lines_for_line_ids( compound_line_list, line_dict, line_num ):#again very bad coding, at some point use more efficient types
  dictn_list = []
  count = line_num
  a = copy.copy(compound_line_list)
  #produces dictionary of line ids for component lines present in each compound line
  a = __recersive_list_gen(\
  a,\
  unzip(copy.copy(line_dict.values()),1),\
  'map(lambda x: x in self.Globals[1][k], self.Globals[0])',\
  Globals = (unzip(copy.copy(line_dict.values())),__list_abs(a))).new_list#should produce{0:[0,0,0,0],1:[0,0,0,0]}
  #splits compound lines based on the change of value in a
  for i in range(len(compound_line_list)):#note a now a dictionary, might not be of correct length, keys for each compound line?, that would make the indexes correct
    clist = copy.copy(compound_line_list[i])
    val = []
    tmp = []
    for j in range(len(a[i])):
      if j == 0 or a[i][j] == a[i][j-1]:
        tmp += [clist[j]]
      else:
        val += [tmp]
        tmp = [clist[j]]
    val += [tmp]
    key = list(enumerate(set(a[i]),count))
    count += len(key)
    dictn_list += zip(key,val)
  line_num += len(dictn_list)
  return dict(dictn_list), line_num
    

"""
this method splits the compound lines for multiple region which have adjacent boundaries
"""

class __split_compound_lines_for_multiple_regions:
  def __init__( self, compound_line_list ):
    self.values = compound_line_list
    for self.itr1 in range(len(self.values)):
      for self.itr2 in range(self.itr1+1,len(self.values)):
        try:
          test = (self.values[self.itr1],self.values[self.itr2])#again possibly unnesicary
        except:
          return
        apre, a1l, apo, s1l, bpre, b1l, bpo = self.__check_for_intersection(self.values[self.itr1],self.values[self.itr2])
        if s1l == []:
          continue
        try:#bad code+probably wrong, might now be unnesicary
          del self.values[self.itr1]
          try:
            del self.values[self.itr2-1]
          except:
            pass
        except:
          pass
        self.values += s1l+apre+bpre+a1l+b1l+apo+bpo
        
        #not currently working
        #vtmp = self.values + self.__check_for_intersection(self.values[self.itr1],self.values[self.itr2])[0]
        #if vtmp == self.values:
          #continue
        #self.values = vtmp
        #del self.values[self.itr1]
        #del self.values[self.itr2-1]
        
  """
  This method is to be implemented and would carry out the intersection
  """
  #note have replaced intersect1d_nu with intersect1d
  #note horribly long - shorten?
  def __check_for_intersection(self,arr1,arr2):
    inset = nset.intersect1d(arr1,arr2)#hopefully based on arr1
    arr2.reverse()
    insetr = nset.intersect1d(arr1,map(lambda x: -x, arr2))#could replace this with numpy array for speed at some point
    arr2.reverse()
    rvs = False
    if insetr.size > inset.size:#note may need to addapt subsiquent code
      inset = insetr
      rvs = True
    if inset.size == 0:
      return [], [], [], [], [], [], []
    br = arr2
    if rvs:
      arr2.reverse()
      br = map(lambda x: -x, arr2)
      arr2.reverse()
    apre = [arr1[:arr1.index(inset[0])]]; apo = [arr1[arr1.index(inset[-1])+1:]]
    bpre = [arr2[:br.index(inset[0])]]; bpo = [arr2[br.index(inset[-1])+1:]]
    ra = range(arr1.index(inset[0]),arr1.index(inset[-1])+1)
    rb = range(br.index(inset[0]),br.index(inset[-1])+1)
    con = 0
    con_s = 0
    flp = 0
    a1l = [[]]
    s1l = [[]]
    for i in ra: #vectorize/mapline_loop_dict.keys()
      if arr1[i] in inset:
        if flp == 1:
          flp = 0
          con_s += 1
          s1l.append([])
        s1l[con_s].append(arr1[i])
        continue
      if flp == 0:
        flp = 1
        con += 1
        a1l.append([])
      a1l[con] += [arr1[i]]
    con = 0
    flp = 0
    b1l = [[]]
    for i in rb:
      if br[i] in inset:
        if flp == 1:
          flp = 0
        continue
      if flp == 0:
        flp = 1
        con += 1
        b1l.append([])
      b1l[con].append(br[i])
    if rvs:
      for i in b1l:
        i.reverse()
        i = map(lambda x: -x, i)
    apre = self.rmvMulti( apre, [] )
    a1l = self.rmvMulti( a1l, [] )
    apo = self.rmvMulti( apo, [] )
    s1l = self.rmvMulti( s1l, [] )
    bpre = self.rmvMulti( bpre, [] )
    b1l = self.rmvMulti( b1l, [] )
    bpo = self.rmvMulti( bpo, [] )
    return [apre,a1l,apo,s1l,bpre,b1l,bpo]

  def rmvMulti( self, lst, val ):#change to extract?,np.extract(arr!=val,val), note arr must be ndarray
    while val in lst:
      lst.remove(val)
    return lst

__list_abs = lambda arr1: map(lambda y: map(lambda x: abs(x), y), arr1)

"""
this method writes the compound line to the geo file

"""
def __write_compound_lines(compound_dict, geo):
  for i in range(len(compound_dict.keys())):
    geo.write("Compound Line(%i) = {%s};\n"%(compound_dict.keys()[i][0],str(compound_dict.values()[i])[1:-1]))

class geometry_writer( object ):

  def GeoWriter( self ):
    """Calls geofile writing methods

    Passed data from define_ids and writes
    mapping between geofile objects and
    their components. Uses these mappings
    to write the geofile

    """

    print "Writing geo file"
    points = self.domainData.pointsList                    # : list of point ordered on shapes and parts
    lines = np.array(self.Lines)                           # : ids to lines, will be repeated
    boundIdMap = np.array(self.IdMap)                      # : this maps lines to there respective Boundry segments
    lloopMap = np.array(self.domainData.LLoopMap)          # : this maps lines to there respective line loops
    boundIds = np.array(self.BoundryIds)                   # : this is the boundry Ids mapped via boundIdMap
    shapeMap = np.array(self.domainData.ShapeMap)          # : this maps lines to there respective shapes
    regionIds = np.array(self.domainData.RegionId)         # : this is the region Ids Mapped via ShapeMap
  
    self.pointIds = self.__generatePoints(points)

    # generating mappings from objects to their components
    if self.Compound: self.IntersectMap = self.__findIntersections(lines,shapeMap)

    #loopcorrect = np.arange(lloopMap.size)#possibly +1

    #boundIdMap[-1] -= loopcorrect[-1]
    #lloopMap -= loopcorrect
    #shapeMap[-1] = loopcorrect[-1]


    if self.Compound: self.CompoundMap = self.__generateCompound(boundIdMap,lloopMap,self.IntersectMap,lines.size)

    if self.Compound: self.LineLoopMap = self.__map_between_objects(self.CompoundMap,lloopMap)
    else: self.LineLoopMap = lloopMap #may work    

    if self.Compound: self.PhysicalLineMap = self.__map_between_objects(self.CompoundMap,boundIdMap)
    else: self.PhysicalLineMap = boundIdMap #watch out for repeats    

    self.PlaneSurfaceMap = np.array([0] + list(self.__map_between_objects(lloopMap,shapeMap)))

    # writing to the geofile
    self.__write_method(points,lines,lloopMap,boundIds,regionIds)
  
  def __define_mapping_from_intersection(self,mapping1,mapping2):
    """Finds section of two arrays which are equal"""
    mp1_outr = np.outer(mapping1,np.ones_like(mapping2))
    mp2_outr = np.outer(np.ones_like(mapping1),mapping2)
    mp_result_outr = np.where(mp1_outr == mp2_outr, mp2_outr, 0)
    return np.sum(mp_result_outr,axis=1)
      
      
  def __generatePoints(self,points):
    """Identifies each point with an Id based on coordinates"""
    pointIds = []
    Idno = 1
    Idmap = {}
    for i in range(len(points)):
      if not (points[i] in points[:i]):
        pointIds += [Idno]
        Idmap[tuple(points[i])] = Idno
        Idno += 1
      else:
        pointIds += [Idmap[tuple(points[i])]]
    return pointIds    
          
  def __findIntersections(self,lines,shapeMap):
    """Determines which lines are shared by multiple shapes"""
    IntersectMap = []
    for s1_Id in range(len(shapeMap)-1):
      for s2_Id in range(len(shapeMap)-1):
        if s1_Id == s2_Id:
          continue
          IntersectMap += [self._define_mapping_from_intersection(lines[shapeMap[s1_Id]:shapeMap[s1_Id+1]],lines[shapeMap[s2_Id]:shapeMap[s2_Id+1]])]
    IntersectMap = np.array(IntersectMap + [len(lines)])
    return np.array([0] + list(IntersectMap[np.nonzero(IntersectMap)]))
      
  def __generateCompound(self,boundIdMap,lloopMap,IntersectMap,line_size):
    """Generates mapping between compounds and lines

    Splits list of lines into the minimum
    number of segments such that no section
    is split by one of the intersect maps     

    """
    CompoundMap = []
    end = False
    Id = 1
    LLnum = 0
    IntersectNum = 0
    BoundIdNum = 0
    while not end:
      n = np.min([boundIdMap[BoundIdNum],lloopMap[LLnum],IntersectMap[IntersectNum]])
      if IntersectMap[IntersectNum] in CompoundMap: continue

      if n == IntersectMap[IntersectNum]: IntersectNum += 1
      if n == lloopMap[LLnum]: LLnum += 1
      if n == boundIdMap[BoundIdNum]: BoundIdNum += 1
      if (n == line_size): end = True

      CompoundMap += [n]
    return np.array(CompoundMap) 
      
  def __map_between_objects(self,ComponentObjects,LineMap):
    ObjectMap = []
    for line_Id in LineMap:
      ObjectMap += [np.sum(np.where(ComponentObjects == line_Id,1,0)*np.arange(ComponentObjects.size))]
    return np.array(ObjectMap)
    

  def __write_method(self,points,lines,lloopMap,boundIds,regionIds):

    #loopcorrect = np.arange(lloopMap.size)
  
    #start writing to file
    self.geofile_inst = open(self.geofilepath,'w')

    #write points
    prev_pointId = 0
    for i in range(len(points)):
      if prev_pointId >= self.pointIds[i]:
        continue
      self.geofile_inst.write("Point(%i) = {%s,0};\n"%(self.pointIds[i], str(points[i])[1:-1]))
      prev_pointId += 1

    #write lines  
    repeatList = []
    Allocated = 0
    LoopNo = 1
    for i in range(len(lines)):
      if i == lloopMap[LoopNo]:
        LoopNo += 1
      if lines[i] <= Allocated:
        continue
      if self.pointIds[i + LoopNo - 1] == self.pointIds[i + LoopNo]:
        repeatList += [lines[i]]
        continue
      self.geofile_inst.write("Line(%i) = {%s};\n" %( lines[i],str([self.pointIds[i + LoopNo - 1],self.pointIds[i + LoopNo]])[1:-1]))
      Allocated += 1
    print 'lines written'


    #print repeatList

    #write compounds
    cLineNo = Allocated + 1 + len(repeatList)
    if self.Compound:
      cLineNo = self.__write_line_objects(cLineNo,self.CompoundMap,"Compound Line(%i) = {%s};\n",lines,0,repeatList)
      print 'compound lines written'    

    #write line loops
    if self.Compound: Components = np.arange(self.CompoundMap.size);ComponentIdStart = lines.size + 1;llrepeatList = []
    else: Components = lines;ComponentIdStart = 0;llrepeatList = repeatList
    cLineNo = self.__write_line_objects(cLineNo,self.LineLoopMap,"Line Loop(%i) = {%s};\n",Components,ComponentIdStart,llrepeatList)
    print 'line loops written'      
  
    #write physical lines
    if self.Compound: Components = np.arange(self.CompoundMap.size);ComponentIdStart = lines.size + 1
    else: 
      Components = lines;ComponentIdStart = 0
      mask = np.ones_like(Components)
      for iD in repeatList:
        mask = np.where(Components==iD,0,mask)
      mask = mask*np.arange(mask.size)
      mask = np.array([0]+list(mask[np.nonzero(mask)]))
      Components = lines[mask]
    self.__write_physical_objects(boundIds,self.PhysicalLineMap,"Physical Line(%i) = {%s};\n",Components,ComponentIdStart)
    print 'physical lines written'    

    #write plane surfaces
    cLineNo = 1
    if self.Compound: ComponentIdStart = lines.size + self.CompoundMap.size
    else: ComponentIdStart = lines.size + 1
    self.__write_line_objects(cLineNo,self.PlaneSurfaceMap,"Plane Surface(%i) = {%s};\n",np.arange(lloopMap.size),ComponentIdStart,[])
    print 'plane surfaces written'  

    #write physical surfaces
    self.__write_physical_objects(regionIds,self.PlaneSurfaceMap,"Physical Surface(%i) = {%s};\n",np.arange(1),1)
    print 'physical surfaces written'

    self.geofile_inst.write('\nMesh.RemeshAlgorithm=1;')

    self.geofile_inst.close()
    print "geo file written : " + self.geofilepath

  def __write_line_objects(self,cLineNo,ObjectMap,ObjectString,Components,ComponentIdStart,repeatList):
    for i in range(len(ObjectMap)-1):
      basear = Components[ObjectMap[i]:ObjectMap[i+1]]
      mask = np.ones_like(basear)
      for iD in repeatList:
        mask = np.where(basear==iD,0,mask)
      mask = mask*np.arange(mask.size)
      mask = np.array([0]+list(mask[np.nonzero(mask)]))
      self.geofile_inst.write(ObjectString % (cLineNo,str(list(basear[mask]  + ComponentIdStart))[1:-1]))
      cLineNo += 1
    return cLineNo


  def __write_physical_objects(self,IdValues,ObjectMap,ObjectString,Components,ComponentIdStart):

    IdsAllocated = []
    cId = IdValues[0]

    while True:

      WithId = []
      for i in range(ObjectMap.size-1):
        if IdValues[i] != cId:
          continue
        WithId += list(Components[ObjectMap[i]:ObjectMap[i+1]]+ComponentIdStart)
      self.geofile_inst.write(ObjectString  % (cId,str(WithId)[1:-1]))
      IdsAllocated += [cId]

      for i in range(ObjectMap.size-1):
        if not (IdValues[i] in IdsAllocated):
          cId = IdValues[i]
          break

      if cId in IdsAllocated:
        break




"""
This method writes the geo and physical ids using the helper emthods defined above.
This method makes sure there are no duplicate lines or points in the geo. The lines 
which are shared are only written once and the same id for the line is used anywhere
else where the same line is in the shape.
@param filepath : specifies the filepath of the geo file to be written
@param data     : specifies the data for teh domains, i.e. the ids and points
"""
def write_geo_file(filepath,data, compound_line_enable, use_bspline):#there should be 1:1 map between line loop and compound lines prior to split

  def __remove_last_line_using_same_point(lines):
    last = lines[-1]
    if last[0]==last[1]:
      lines.pop()
    return lines
  region_id = data[0]
  
  if use_bspline:
    line_string = "BSpline"
  else:
    line_string = "Line"

  shapes_index = data[1]
  boundary_id = data[2]
  domain_points = data[3]
  #remove the last line which has same point twice

  map(__remove_last_line_using_same_point, domain_points)
  if ".geo" not in filepath:
    filepath += ".geo"

  #add the end of last shape to the shapes_index array
  shapes_index.append(len(domain_points))
  try:
    #open the file to write the geo file
    geo = open(filepath,"w")
    print "Writing geo file"
    #define the loop variants being used by the following
    point_dict = {}
    line_dict = {}
    line_loop_dict = {}
    line_index = -1
    surface_dict = {}
    line_num = 1
    line_loop_num = 1
    point_num = 1
    surface_num = 1
    shape_number = -1
    p_surface_dict = {}

    #loop for every shape. each shape contains some islands so split points are used
    for i in range(len(shapes_index)-1):
      surface_line_loops = []
      #loop for every line loop in each shape. i.e. boundary and islands
      for line_loop in domain_points[shapes_index[i]:shapes_index[i+1]]:
        compound_line = []
        prev_line_pid = -1
        shape_number += 1
        line_in_line_loop = []
        line_index = -1
        for line in line_loop:
          line_index += 1
          points_in_line = []
          for p in line:
            try:
              #check if the current point already exists
              point_id = point_dict[tuple(p)]
              points_in_line.append(point_id)
            except KeyError:
              #write the point to geo file and add it to the dictionary
              point_dict[tuple(p)] = point_num
              points_in_line.append(point_num)
              geo.write("Point(%i) = {%s,0};\n"%(point_num, str(p)[1:-1]))
              point_num += 1
          try :
            #check if the current line has already been written
            line_id,line_pid = line_dict[tuple(points_in_line)]
            line_in_line_loop.append(line_id)
          except KeyError:
            try :#this section is wrong for some reason
              #check if the line in opposite direction exists
              reverse_line = points_in_line + []
              reverse_line.reverse()
              line_id,line_pid = line_dict[tuple(reverse_line)]
              line_in_line_loop.append(0-line_id)
            except KeyError:
              #if the line has not yet been written then write the file and add to the dictionary
              line_pid = boundary_id[shape_number][line_index]
              line_dict[tuple(points_in_line)] = (line_num,line_pid)
              line_in_line_loop.append(line_num)
              geo.write("%s(%i) = {%s};\n" %(line_string, line_num,str(points_in_line)[1:-1]))
              line_num += 1
        try:
          #check if the current line loop already exists
          line_loop_id = line_loop_dict[tuple(line_in_line_loop)]
          surface_line_loops.append(line_loop_id)
        except KeyError:
          #check for reverse line loop
          try :
            reverse_loop = line_in_line_loop + []
            reverse_loop.reverse()
            line_loop_id = line_loop_dict[tuple(reverse_loop)]
            surface_line_loops.append(0-line_loop_id)
          except KeyError:
            #write a new line loop
            line_loop_dict[tuple(line_in_line_loop)] = line_loop_num
            surface_line_loops.append(line_loop_num)
            if not compound_line_enable:
              geo.write("Line Loop(%i) = {%s};\n" % (line_loop_num,str(line_in_line_loop)[1:-1]))
            line_loop_num += 1#don't change this
      if not compound_line_enable:
        surface_pid = region_id[shapes_index[i]]
        try :
          surface_pid_list = surface_dict[surface_pid]
          surface_pid_list.append(surface_num)
        except KeyError:
          surface_dict[surface_pid] = [surface_num]
        p_surface_dict[surface_num] = surface_line_loops
        geo.write("Plane Surface(%i) = {%s};\n" % (surface_num,str(surface_line_loops)[1:-1]))
        surface_num +=1
    if compound_line_enable:
      print 'lines written'
      compound_line_list_b = map(list,line_loop_dict.keys())
      if len(shapes_index)>1:
        compound_line_list = __split_compound_lines_for_multiple_regions(copy.copy(compound_line_list_b)).values
      compound_line_dict, line_num = __split_compound_lines_for_line_ids(compound_line_list,line_dict,line_num)#note currently incompatible with line id's
      compound_line_dict = dict(zip(compound_line_dict.keys(),__list_abs(compound_line_dict.values())))
      __write_compound_lines(compound_line_dict,geo)
      print 'compounds written'
      
      line_loop_line = __recersive_list_gen(\
      line_loop_dict.keys(),\
      unzip(compound_line_dict.keys()),\
      'map(lambda x, nset = nset: nset.intersect1d(x,self.Globals[1][k]).size != 0, self.Globals[0])',\
      Globals = (compound_line_dict.values(),__list_abs(line_loop_dict.keys()))).new_list#possiblity reordering occuring here, can keys be reorder at all (or do it post creating dictionary)
      line_loop_dict = dict(enumerate(line_loop_line.values(), line_num))#note too many when there is complete intersection, may not matter too much, note this is fine res ordering
      for key in line_loop_dict.keys():#these might not be correct/or possibly the compound lines
        geo.write("Line Loop(%i) = {%s};\n" % (key,str(list(line_loop_dict[key]))[1:-1]))
      print 'line loops written'
      prev = [0]
      xkeys = line_loop_dict.keys()
      xkeys.reverse()#this isn't ordered correctly for some reason, where is this being ordered. note pre-lineloops is correct, its a dictionary, most likely resulting in the lack of order
      #order xkeys according to line_loop_dict.values?
      #what order should they be in?
      xval = line_loop_dict.values()
      mnval = map(min,xval) #possibly use numpy min
      #xval.reverse()
      mnval.reverse()
      xkeys2 = []
      #wrong order
      print 'begin'
      for i in range(len(mnval)):
        for j in range(len(xval)):
          if mnval[i] in xval[j]:
            xkeys2 += [xkeys[j]]
            del xval[j]
            del xkeys[j]
            break
      for i in range(len(shapes_index)-1):
        #if max(_flatten(map(list,line_loop_dict.values()[shapes_index[i]:shapes_index[i+1]]))) < max(prev):#note some of the indexes are the wrong way round
          #crnt = xkeys[shapes_index[prev_i]:shapes_index[i+1]]
          #print crnt
          #geo.write("Plane Surface(%i) = {%s};\n" % (surface_num,str(crnt)[1:-1]))
          #continue
        crnt = xkeys2[shapes_index[i]:shapes_index[i+1]]
        geo.write("Plane Surface(%i) = {%s};\n" % (surface_num,str(crnt)[1:-1]))
        #prev = _flatten(map(list,line_loop_dict.values()[shapes_index[i]:shapes_index[i+1]]))
        #prev_i = i
        surface_num +=1
      print 'Planes Written'
      __write_compound_lines_as_physical( compound_line_dict,geo )#hopefully doesn't need changing
      print 'Physical Lines Written'
      #may want to make sure shape_loop_list isn't called
      physical_list = {}
      for i in range(len(shapes_index)-1):
        try:
          physical_list[region_id[shapes_index[i]]]
          physical_list[region_id[shapes_index[i]]] += [i+1]
        except:
          physical_list[region_id[shapes_index[i]]] = [i+1]
          continue
      #note sometimes reverse of physical_line_list - thought this may not work in all situations 
      for key in physical_list.keys():
        geo.write("Physical Surface(%i) = {%s};\n" % (key,str(physical_list[key])[1:-1]))
      print 'Surfaces Written'
    else :
      __write_physical_lines_to_geo(line_dict.values(),geo)#sort out Physical Lines!
      __write_physical_surface_list_obs(region_id, len(shapes_index), geo)

    geo.write("\n\nMesh.RemeshAlgorithm=1;\n")
    geo.close()
    print "geo file written : " + filepath
  except IOError:
    print "Error: An error occurred while writing the geo file"
    QMessageBox.critical(None,"Error: In Writing Geo File","An error has occurred while writing the geo file")
    raise AssertionError

 
"""
This method uses a text file generated by the data given from the define id script.
"""
def test_with_txt_file():
  filepath = "shapefile_data_simplified.txt"
  data = open(filepath,"r")
  lines = data.readlines()
  data = [lines[1],lines[4],lines[7],lines[10]]
  data = map(eval,data)
  write_geo_file("antartica_multiple_domain.geo",data)
