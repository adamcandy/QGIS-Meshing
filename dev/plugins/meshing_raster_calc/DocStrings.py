class a:

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

	"""float division of arr1 by arr2. returns
	lim instead of yeilding a zero error"""

class b:
	"""replaces elements set to lim in arr with a value set as
	being an order of magnitude higher than the square of the 
	maximum value of arr.  converts all elements of arr to
	numpy.float64 dtype"""

class c:
	"""diferentiates field with respect to withRespectTo.
	arguments must be 1 dimensional numpy arrays.  assumes 
	elements in these arrays represent points on a continuous 
	mathmatical function. returns result as an array"""

class d:
	"""integrates field with respect to withRespectTo.
	arguments must be 1 dimensional numpy arrays.  assumes 
	elements in these arrays represent points on a continuous 
	mathmatical function. returns result as an array.  c is
	the constant of integration and defaults to zero"""

class e:
	"""appies a python function function which opperates on psi and lon"""

class f:
	"""appies a python function function which opperates on psi and lat"""

class g:
	"""calculates the divergence of psi with respect to lat
	and lon.  returns result as a numpy array with the same 
	shape as psi"""

class h:
	"""calculates the surface integral of psi with respect to
	lat and lon.  returns result as a numpy array with the same
	shape as psi"""

class i:
	"""retreaves the netCDF file entered as a string in the argument.
	returns the lat,lon and z variables as lat,lon and psi"""
