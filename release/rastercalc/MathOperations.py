from standardModules import *

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

x   = []
y   = []
lon = []
lat = []
psi = [] #this seems to be causing problems with the f_lat,f_lon and Divergence
lim = 'lim'

def retrieveLatLon_obs(Field):
	lengthlat = Field.shape[1]
	lengthlon = Field.shape[0]
	lat = np.linspace(0,lengthlat,lengthlat+1)
	lon = np.linspace(0,lengthlat,lengthlat+1)
	return lat, lon

def retrieveLatLon(Field): #rewrite to use data from spaceData; note propotionality might be off
	lengthLat = Field.shape[1]
	lengthLon = Field.shape[0]
	lat = np.linspace(0,lengthLat,lengthLat)
	lon = np.linspace(0,lengthLon,lengthLon)
	latField = np.outer(np.ones(lengthLon), lat)
	lonField = np.outer(np.ones(lengthLat), lon)
	Field = latField + lonField.transpose()
	result = getHyp(Field)
	return result

def getHyp(arr):
	infinityPart = np.zeros_like(arr)
	hyperR = np.array([arr,infinityPart], dtype = np.float64)
	return hyperR

def division(arr1, arr2):
	a1 = arr1[0]
	a2 = arr1[1]
	b1 = arr2[0]
	b2 = arr2[1]
	c1 = np.where(np.logical_and(b1 == 0,a1 == 0), 1, np.where(b1 == 0, a1, a1/b1))
	c2 = np.where(np.logical_or(b1 != 0,a1 == 0), a2-b2, 1+a2-b2)
	result = np.array([c1,c2])
	return result

def mult(arr1, arr2):
	a1 = arr1[0]
	a2 = arr1[1]
	b1 = arr2[0]
	b2 = arr2[1]
	c1 = np.where(b1 == 0, a1, np.where(a1 == 0, b1, a1*b1))
	c2 = np.where(np.logical_and(a1 != 0, b1 != 0), a2+b2, a2+b2-1)
	result = np.array([c1,c2])
	return result

def add(arr1, arr2): #note using -arr2 is inaccurate
	a1 = arr1[0]
	a2 = arr1[1]
	b1 = arr2[0]
	b2 = arr2[1]
	c1 = np.where(a2 == b2, a1+b1, np.where(a2 > b2,a1,b1))
	c2 = np.where(a2>b2,a2,b2)
	result = np.array([c1,c2])
	return result

def take(arr1, arr2):
	a1 = arr1[0]
	a2 = arr1[1]
	b1 = arr2[0]
	b2 = arr2[1]
	c1 = np.where(a2 == b2, a1-b1, np.where(a2 > b2,a1,b1))
	c2 = np.where(a2>b2,a2,b2)
	result = np.array([c1,c2])
	return result

def shift(arr, val = 1):
	c1 = shiftPart(arr[0],val)
	c2 = shiftPart(arr[1],val)
	return np.array([c1,c2])

def shiftPart(arr, val): #possibly generalise at some point
	a = np.roll(arr,val).transpose()
	if val > 0:
		a[val-1] = np.zeros_like(a[val-1])
	elif val < 0:
		a[val] = np.zeros_like(a[val])
	result = a.transpose()
	return result

def flip(arr1):
	c1 = arr1[0].transpose()
	c2 = arr1[1].transpose()
	result = np.array([c1,c2])
	return result

def difDirection(arr1,arr2):
#now yielding roughly correct result, may have a diferent constant of porpotionality
	del_field = take(shift(arr1,1),shift(arr1,-1))
	del_par =  take(shift(arr2,1),shift(arr2,-1))
	result = division(del_field, del_par)
	return result

def checkZeroLim(arr):#write into code later
	a1 = arr[0]
	a2 = arr[1]
	c1 = np.where(a1 != 0, a1, 1)
	c2 = np.where(a1 != 0, a2, a2-1)
	return np.array([c1,c2])

def diferentialOp(arr1, arr2):
	print 'ddx'
	ddx = difDirection(arr1,arr2)
	print 'ddy'
	ddy = flip(difDirection(flip(arr1),flip(arr2)))
	return ddx, ddy

def intOp(field, withRespectTo, c = 0.0):
	DocStrings.d.__doc__
	result = []
	shp = field.shape
	int_field = np.array([c])
	for i in range(field.size): 
		if i > 0 and i < (field.size - 1):
			av_field1 = (3*field[i]+field[i-1])
			av_field2 = (3*field[i]+field[i+1])
			del_par1  = (withRespectTo[i]-withRespectTo[i-1])
			del_par2  = (withRespectTo[i+1]-withRespectTo[i])
		elif i == 0:
			av_field1 = (field[1]+3*field[0])
			av_field2 = av_field1
			del_par1  = (withRespectTo[1]-withRespectTo[0])
			del_par2  = del_par1
		else:
			av_field1 = (3*field[i]+field[i-1])
			av_field2 = av_field1
			del_par1  = (withRespectTo[i]-withRespectTo[i-1])
			del_par2  = del_par1
		int_field += (av_field1*del_par1+av_field2*del_par2)/8.0
		result.append(copy.copy(int_field))
	result = np.array(result)
	result.shape = shp
	return result


def f_lon(function, psi = psi,lon = lon): #could define this as a method of psi? is now a method of mathOp
	DocStrings.e.__doc__
	result = np.zeros(psi.shape)
	for i in range(psi.shape[0]):
		result[i] = function(psi[i], lon)
	return result 

def f_lat(function, psi = psi,lat = lat):
	DocStrings.f.__doc__
	psi = psi.transpose()
	result = np.zeros(psi.shape)
	for i in range(psi.shape[0]):
		result[i] = function(psi[i],lat)
	result = result.transpose()
	return result

def logNatural(arr):
	a1 = arr[0]
	a2 = arr[1]
	c1a = np.where(a1 != 0, np.log(a1), -1)
	c2a = np.where(a1 != 0, 0, 1)
	trm1 = checkZeroLim(np.array([c1a,c2a]))
	trm2 = checkZeroLim(np.array([a2,np.ones_like(a2)]))
	result = add(trm1,trm2)
	return result

'''
def logN(arr1,arr2 = 'ten'):
	if arr2 == 'ten':
		arr2 = getHyp(np.zeros_like(arr1[0])+10)
	a1 = arr1[0]
	a2 = arr1[1]
	b1 = arr2[0]
	b2 = arr2[1]
	one = np.ones_like(a2)
	c1a = np.where(a1 != 0, np.log(a1), -1)
	c2a = np.where(a1 != 0, 0, 1)
	c = checkZeroLim(np.array([c1a,c2a])) #may be a faster implimentation of this
	c1a = c[0]; c2a = c[1]
	
	alpha1 = np.where(c2a == one, c1a+a2, np.where(c2a > one,c1a,a2))
	alpha2 = np.where(c2a>one,c2a,one)
	d1a = np.where(b1 != 0, np.log(b1), -1)
	d2a = np.where(b1 != 0, 0, 1)
	d = checkZeroLim(np.array([d1a,d2a]))
	d1a = d[0]; d2a = d[1]
	beta1 = np.where(d2a == one, d1a+b2, np.where(d2a > one,d1a,b2))
	beta2 = np.where(d2a>one,d2a,one)
	gamma1 = np.where(np.logical_and(beta1 == 0,alpha1 == 0), 1, np.where(beta1 == 0, alpha1, alpha1/beta1))
	gamma2 = np.where(np.logical_or(beta1 != 0,alpha1 == 0), alpha2-beta2, 1+alpha2-beta2)
	result = np.array([gamma1,gamma2])
	return result
'''

def logN(arr1,arr2 = 'ten'):
	if arr2 == 'ten':
		arr2 = getHyp(np.zeros_like(arr1[0])+10)
	a = logNatural(arr1)
	b = logNatural(arr2)
	result = division(a,b)
	return result
	
def intFields(Field1, Field2, param1, c=0): #again may adapt to work in lat, curently c has no effect
	a = f_lon(diferentialOp, Field2, param1)#this may not be accurate
	arr = Field1*a
	result = f_lon(intOp, arr, param1)
	return result

def returnReal(arr): #note returns 0 for inf^-n #minor inaccuracy this is returning 0*inf as 0 rather than 1
	a1 = arr[0]
	a2 = arr[1]
	#a1 = np.where(a1==a1+1,1,a1)
	inf = np.max(np.abs(arr))*10
	if inf == inf + 1:
		inf = np.max(np.abs(a1))
	order = np.where(a2 < 0, 0, inf**a2)
	resultTemp = arr[0]*order
	#resultTemp = np.where(resultTemp==resultTemp+1,0,resultTemp)
	#inf = np.max(np.max(np.abs(resultTemp)),inf)
	#result = np.where(resultTemp==resultTemp+1,inf,resultTemp)
	return resultTemp

def diferentiateLat(Field):
	print 'dif x1'
	l = retrieveLatLon(Field)
	f = getHyp(Field)
	psi = diferentialOp(f, l)[1]
	return returnReal(psi) #can still do this

def divergence(Field):
	print 'dvg'
	l = retrieveLatLon(Field)
	f = getHyp(Field)
	psi = diferentialOp(f, l)
	phi = add(psi[0],psi[1])
	result = returnReal(phi)
	return result

def diferentiateFields(Field1, Field2):
	print 'dif f'
	f = getHyp(Field1)
	g = getHyp(Field2)
	psi = diferentialOp(f, g)
	F = add(psi[0],psi[1])
	return returnReal(F)

def diferentiateLon(Field):
	print 'dif x0'
	l = retrieveLatLon(Field)
	f = getHyp(Field)
	psi = diferentialOp(f, l)[0]
	return returnReal(psi)

def divisionLim(Field1, Field2):
	print 'div'
	if not (isinstance(Field1,np.ndarray) and isinstance(Field1,np.ndarray)):
		if isinstance(Field1,np.ndarray):
			a = np.ones_like(Field1)
			Field2 = a*Field2
		else:
			a = np.ones_like(Field2)
			Field1 = a*Field1
	f = getHyp(Field1)
	g = getHyp(Field2)
	psi = division(f, g)
	result = returnReal(psi)
	return result

def integralLat(field):
	lat = retrieveLatLon_obs(field)[0]
	result = f_lat(intOp, field, lat)
	return result

def integralLon(field):
	lon = retrieveLatLon_obs(field)[1]
	result = f_lon(intOp, field, lon)
	return result

def surfaceIntegral(field):
	result = integralLat(field) + integralLon(field)
	return result

def integrateFields(Field1, Field2):
	lat = retrieveLatLon_obs(Field1)[0]
	result = intFields(Field1, Field2, lat)
	return result

def lnLim(Field): #add in default at some point
	#if not isinstance(Field,np.array):
		#	a = np.ones_like(default)
			#Field = a*Field
	print 'ln'
	f = getHyp(Field)
	psi = logNatural(f)
	result =  returnReal(psi)
	return result

def logLim(tup): #note need to change rastcalc engine
	print 'logN'
	Field1 = tup[0]
	if tup.shape[0] == 2:
		Field2 = tup[1]
	else:
		Field2 = 10
	print 'N:', Field2
	if not (isinstance(Field1,np.ndarray) and isinstance(Field2,np.ndarray)):
		if isinstance(Field1,np.ndarray):
			a = np.ones_like(Field1)
			Field2 = a*Field2
		else:
			a = np.ones_like(Field2)
			Field1 = a*Field1
	f = getHyp(Field1)
	g = getHyp(Field2)
	psi = logN(f, g)
	return returnReal(psi)



def multimin(tup):
	var = 0.0
	for i in tup:
		if isinstance(var, float):
			var = i
		else:
			var = np.minimum(i,var)
	return var

def multimax(tup):
	var = 0.0
	for i in tup:
		if isinstance(var, float):
			var = i
		else:
			var = np.maximum(i,var)
	return var

		
