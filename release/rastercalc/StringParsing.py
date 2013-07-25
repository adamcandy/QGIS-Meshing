

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

class superstring:
	def __init__(self, BaseString):
		self.BaseString = BaseString

	def strip(self):
		self.BaseString = self.BaseString.strip()
	def swapcase(self):
		self.BaseString = self.BaseString.swapcase(arg)
	def replace(self, arg1, arg2):
		self.BaseString = self.BaseString.replace(arg1, arg2)

	def seperate(self, item):
		a1 = [i for i in self.BaseString]
		a2 = []
		par = ''
		for i in a1:
			if i != item:
				par.append(i)
				continue
			if par != ''
				a2.append(par)
			a2.append(i)
			par = ''
		return a1
		
	def transform(self, dikt)
		for i in dikt.keys()
			self.replace(i, dikt[i])

	class dualities:
		self.dualityIds = []
		self.current = None
		def newDuality(self):
			Id = len(self.dualityIds)
			self.dualityIds.append(Id)
		def callDuality(self):
			

	class duality(dualities):
		def __init__(self, lst):
			kys = [i for i in range(len(lst)]
			kys = tuple(kys)
			self.dikt =	dict([(i, lst[i]) for i in kys])
			dualities.newDuality()
			self.Id = dualities.dualityIds[len(dualityIds)-1]




def pythoninput(x):
	a1 = map(str, filter(None, (i.strip() for i in x.split('('))))
	a2 = []
	for k in range(len(a1)):
		a2 += copy.copy(map(str, filter(None, (i.strip() for i in a1[k].split(',')))))
	a3 = a2							# change at somepoint
	a4 = []
	countup = 0
	countback = 0
	while (countup+countback)  < len(a3):
		var = -(1+countback)
		if ')' in a3[var]:
			a4 +=[a3[countup]]
			a4 +=[' ']
			countup += 1
			a3[var] = a3[var][:-1]
		else:
			a4 += [a3[var]]
			a4 += [' ']
			countback += 1
	a4.reverse()
	result = ''
	for i in a4:
		result += copy.copy(i)
	result = result.replace(')','')
	return result
