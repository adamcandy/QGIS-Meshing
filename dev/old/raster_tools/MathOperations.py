from standardModules import *

x   = []
y   = []
lon = []
lat = []
psi = [] #this seems to be causing problems with the f_lat,f_lon and Divergence
lim = 'lim'

def mult(arr1, arr2): #possibly temporary
		result = arr1*arr2
		return result

def division(arr1,arr2):
	DocStrings.a.__doc__
	if arr2 != 0:
		result = arr1/float(arr2)
	elif arr1 == 0:
		result = 1
	else:
		result = lim
	return result

def resolveLim(arr):
	DocStrings.b.__doc__
	locv = copy.copy(arr)
	for k in range(arr.size):
		if locv.flat[k] == lim:
			locv.flat[k] = 0
	locv = locv.astype(float)
	locv *= locv	
	mx = locv.max()
	for k in range(arr.size):
		if arr.flat[k] == lim:
			arr.flat[k] = 10*mx
	for i in arr.flat:
		i = np.float64(i)
	return arr

def opLim(func,arr1,arr2):
		result = np.zeros(arr1.shape)
		for i in range(arr1.size):
			if arr1[i] != lim and arr2[i] != lim:
				result[i] = func(arr1[i],arr2[i])
			else:
				result[i] = lim
		return result

def diferentialOp(field, withRespectTo):
	DocStrings.c.__doc__
	result = []
	for i in range(field.size):
		if i > 0 and i < (field.size-1):
			del_field = (field[i+1]-field[i-1])/2.0
			del_par   = (withRespectTo[i+1]-withRespectTo[i-1])/2.0
		elif i == 0:
			del_field = (field[1]-field[0])/2.0
			del_par   = (withRespectTo[1]-withRespectTo[0])/2.0
		else:
			del_field = (field[i]-field[i-1])/2.0
			del_par   = (withRespectTo[i]-withRespectTo[i-1])/2.0
		if isinstance(del_field, float) == True:# is this still nesicary?
			dif_field = division(del_field,del_par)
		result.append(dif_field)
	result = np.array(result)
	result = resolveLim(result)
	return result

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

def divergenceOfField(psi = psi, lat = lat, lon = lon):  #at time of definition getfield has not been called
	DocStrings.g.__doc__
	ddlon = f_lon(diferentialOp, psi, lon)				 #so this will default to the empty list of original 
	ddlat = f_lat(diferentialOp, psi,lat)                #parametre definition
	result = ddlon + ddlat
	return result

def surfaceIntegral(psi = psi, lat = lat, lon = lon): #note can c be included in this definition
	DocStrings.h.__doc__
	inlon = f_lon(intOp, psi, lon)
	inlat = f_lat(intOp, psi, lat)
	result = inlon + inlat
	return result

def diferentiateFields(Field1, Field2, param1): #may adapt to work in lat as well for accuracy
	a = f_lon(diferentialOp, Field2, param1)    
	ones = np.zeros(a.shape) + 1
	for i in a:
		i = f_lon(division,ones,i)
	ddlon = f_lon(diferentialOp, Field1, param1)
	opLim(mult,ddlon,a)
	result = resolveLim(result)
	return result
	
def intFields(Field1, Field2, param1, c=0): #again may adapt to work in lat, curently c has no effect
	a = f_lon(diferentialOp, Field2, param1)#this may not be accurate
	arr = Field1*a
	result = f_lon(intOp, arr, param1)
	return result
