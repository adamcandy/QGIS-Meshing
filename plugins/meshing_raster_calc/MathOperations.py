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

def cumsumtemp(arr): #revise
	a1 = arr[0]
	a2 = arr[1]
	c1 = np.cumsum(a1,axis=1)
	c2 = np.cumsum(a1,axis=1)#this will be problematic
	return np.array([c1,c2])

def intDirection(arr1,arr2):
	three = getHyp(np.zeros_like(arr1[0])+3)
	eight = getHyp(np.zeros_like(arr1[0])+8)
	av_fieldForward = add(mult(three,arr1), shift(arr1,1))
	av_fieldBack = add(mult(three,arr1), shift(arr1,-1))
	del_parForward = take(shift(arr2,1),arr2)
	del_parBack = take(arr2,shift(arr2,-1))
	int_field = division(add(mult(av_fieldForward,del_parForward), mult(av_fieldBack,del_parBack)), eight)
	#result = cumsumtemp(int_field)#tends to infinity
	result = int_field
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

def intOp(arr1, arr2): #possibly add in c=0.0
	print 'intx'
	intx = intDirection(arr1,arr2)
	print 'inty'
	inty = flip(intDirection(flip(arr1),flip(arr2)))
	return intx, inty

'''#this is not relivent until rastercalc is changed to completly work with hypereals
def power(arr1, arr2): #note wrong + somewhat unimportant
	a1 = arr1[0]
	a2 = arr1[1]
	b1 = arr2[0]
	b2 = arr2[1]
	b1 = getHyp(b1)
	a2 = getHyp(a2)
	c1 = mult(b1,a2)
	c2 = b2 + 1 + c1[1]
	return np.array([c1[0],c2])
'''

def logNatural(arr):
	a1 = arr[0]
	a2 = arr[1]
	c1a = np.where(a1 != 0, np.log(a1), -1)
	c2a = np.where(a1 != 0, 0, 1)
	trm1 = checkZeroLim(np.array([c1a,c2a]))
	trm2 = checkZeroLim(np.array([a2,np.ones_like(a2)]))
	result = add(trm1,trm2)
	return result

def logN(arr1,arr2 = 'ten'):
	if arr2 == 'ten':
		arr2 = getHyp(np.zeros_like(arr1[0])+10)
	a = logNatural(arr1)
	b = logNatural(arr2)
	result = division(a,b)
	return result

def returnReal(arr): #note returns 0 for inf^-n #minor inaccuracy this is returning 0*inf as 0 rather than 1
	a1 = arr[0]
	a2 = arr[1]
	#a1 = np.where(a1==a1+1,1,a1)
	inf = np.max(np.abs(arr))*10
	if inf == inf + 1:
		inf = np.max(np.abs(arr))
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

def integralLat(Field):
	print 'int x1'
	l = retrieveLatLon(Field)
	f = getHyp(Field)
	psi = intOp(f, l)[1]
	real = returnReal(psi)
	result = np.cumsum(real,axis = 0)
	return result

def integralLon(Field):
	print 'int x0'
	l = retrieveLatLon(Field)
	f = getHyp(Field)
	psi = intOp(f, l)[0]
	real = returnReal(psi)
	result = np.cumsum(real,axis = 1)
	return result

def surfaceIntegral(Field):
	print 'int surface'
	l = retrieveLatLon(Field)
	f = getHyp(Field)
	psi = intOp(f, l)
	real1 = returnReal(psi[0])
	real2 = returnReal(psi[1])
	result = np.cumsum(real1,axis = 1) + np.cumsum(real2,axis = 0) #warning prone to infinities
	return result

def integrateFields(Field1, Field2):
	print 'int f'
	f = getHyp(Field1)
	g = getHyp(Field2)
	psi = intOp(f, g)
	real1 = returnReal(psi[0])
	real2 = returnReal(psi[1])
	result = np.cumsum(real1,axis = 1) + np.cumsum(real2,axis = 0)
	return result

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
def multLim(Field1, Field2):
	if not isinstance(Field1,np.array) and isinstance(Field1,np.array):
		if isinstance(Field1,np.array):
			a = np.ones_like(Field1)
			Field2 = a*Field2
		else:
			a = np.ones_like(Field2)
			Field1 = a*Field1
	f = getHyp(Field1)
	g = getHyp(Field2)
	psi = mult(f, g)
	return returnReal(psi)

def addLim(Field1, Field2):
	if not isinstance(Field1,np.array) and isinstance(Field1,np.array):
		if isinstance(Field1,np.array):
			a = np.ones_like(Field1)
			Field2 = a*Field2
		else:
			a = np.ones_like(Field2)
			Field1 = a*Field1
	f = getHyp(Field1)
	g = getHyp(Field2)
	psi = add(f, g)
	return returnReal(psi)

def takeLim(Field1, Field2):
	if not isinstance(Field1,np.array) and isinstance(Field1,np.array):
		if isinstance(Field1,np.array):
			a = np.ones_like(Field1)
			Field2 = a*Field2
		else:
			a = np.ones_like(Field2)
			Field1 = a*Field1
	f = getHyp(Field1)
	g = getHyp(Field2)
	psi = take(f, g)
	return returnReal(psi)

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

		
