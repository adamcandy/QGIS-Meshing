# -*- coding: utf-8 -*-

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

#******************************************************************************
#
# RasterCalc
# ---------------------------------------------------------
# Raster manipulation plugin.
#
# Based on rewritten rasterlang plugin (C) 2008 by Barry Rowlingson
#
# Copyright (C) 2009 GIS-Lab (http://gis-lab.info) and
# Alexander Bruy (alexander.bruy@gmail.com)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/copyleft/gpl.html>. You can also obtain it by writing
# to the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.
#
#******************************************************************************

from __future__ import division

import re
import numpy
import MathOperations
from PyQt4.QtGui import *
from pyparsing import Word, alphas, ParseException, Literal, CaselessKeyword, \
     Combine, Optional, nums, Or, Forward, ZeroOrMore, StringEnd, alphanums, \
     Regex

import rastercalcutils as rasterUtils

exprStack = []
rasterNames = set()

def rasterName():
  return Combine( "[" + Word( alphas + nums, alphanums + "._-" ) + "]" ) 

def pushFirst( str, loc, toks ):
    global exprStack
    
    exprStack.append( toks[0] )

def getBand( data, n ):
  n = n - 1
  if len( data.shape ) == 3:
    return data[ int( n ) ]
  if len( data.shape ) == 2 and n == 1:
    return data
  if len( data.shape ) == 2:
    if n == 0:
      return data
    else:
      raise ValueError, "can't get band " + str( n ) + " from single-band raster"
  raise ValueError, "array must be with 2 or 3 dimensions"

def assignVar( str, loc, toks ):
    global rasterNames
    rasterNames.add( toks[ 0 ] )
    return toks[ 0 ]

def returnRaster( layerName ):
  return rasterUtils.getRaster( layerName )

def returnBand( layerName, bandNum, row, size, count ):
  return rasterUtils.getRasterBand( layerName, bandNum, row, size, count )

# conditional operators
def equal( raster, compare, replace ):
  tmp = numpy.equal( raster, compare )
  numpy.putmask( raster, tmp, replace )
  return raster

def greater( raster, compare, replace ):
  tmp = numpy.greater( raster, compare )
  numpy.putmask( raster, tmp, replace )
  return raster

def less( raster, compare, replace ):
  tmp = numpy.less( raster, compare )
  numpy.putmask( raster, tmp, replace )
  return raster

def not_equal( raster, compare, replace ):
  tmp = numpy.not_equal( raster, compare )
  numpy.putmask( raster, tmp, replace )
  return raster

def greater_equal( raster, compare, replace ):
  tmp = numpy.greater_equal( raster, compare )
  numpy.putmask( raster, tmp, replace )
  return raster

def less_equal( raster, compare, replace ):
  tmp = numpy.less_equal( raster, compare )
  numpy.putmask( raster, tmp, replace )
  return raster

# define grammar
point = Literal( '.' )
colon = Literal( ',' )

e = CaselessKeyword( 'E' )
plusorminus = Literal( '+' ) | Literal( '-' )
number = Word( nums )
integer = Combine( Optional( plusorminus ) + number )
floatnumber = Combine( integer +
                       Optional( point + Optional( number ) ) +
                       Optional( e + integer )
                     )

ident = Combine( "[" + Word( alphas + nums, alphanums + "._-" ) + "]" )
fn = Literal("exp") | Literal("log") | Literal("intS") | Literal("intF") | Literal("inty") | Literal("intx") | Literal("ddy") | Literal("ddx") | Literal("sin") | Literal("asin") | Literal("cos") | Literal("acos") | Literal("tan") | Literal("atan") | Literal("ddF") | Literal("dvg") | Literal("Mmin") | Literal("Mmax") | Literal("sqrt") | Literal("atan2") | Literal("log10") | Literal("eq") | Literal("ne") | Literal("lt") | Literal("gt") | Literal("le") | Literal("ge")| Literal("min")| Literal("max")| Literal("pow")| Literal("ln") | Literal("abs") 

plus  = Literal( "+" )
minus = Literal( "-" )
mult  = Literal( "*" )
div   = Literal( "/" )
lpar  = Literal( "(" )
rpar  = Literal( ")" )

equal_op         = Literal( "=" )
not_equal_op     = Literal( "!=" )
greater_op       = Combine( Literal( ">" ) + ~Literal( "=" ) )
greater_equal_op = Combine( Literal( ">" ) + Literal( "=" ) )
less_op          = Combine( Literal( "<" ) + ~Literal( "=" ) )
less_equal_op    = Combine( Literal( "<" ) + Literal( "=" ) )

addop  = plus | minus
multop = mult | div
compop = less_op | greater_op | less_equal_op | greater_equal_op | not_equal_op | equal_op
expop = Literal( "^" )
band = Literal( "@" )



args = 1



expr = Forward()


atom = ( ( e 
          | floatnumber 
          | integer 
          | (ident).setParseAction( assignVar ) + band + integer
          | fn + lpar + expr + ZeroOrMore(colon + expr) + rpar
          ).setParseAction(pushFirst)
          ( lpar + expr + rpar )
       )

factor = Forward()
factor << (atom | expr)

term =  (factor | expr) + ZeroOrMore( multop + expr )
addterm = (term | expr) + ZeroOrMore(  addop + expr )
expr << ((lpar + expr + rpar) | addterm)
bnf = expr

pattern =  bnf + StringEnd()

# map operator symbols to corresponding arithmetic operations
opn = { "+" : ( lambda a,b: numpy.add( a, b ) ),
        "-" : ( lambda a,b: numpy.subtract( a, b ) ),
        "*" : ( lambda a,b: numpy.multiply( a, b ) ),
        "/" : ( lambda a,b: MathOperations.divisionLim( a, b ) ),
        "^" : ( lambda a,b: numpy.power( a, b) ),
        "<" : ( lambda a,b: numpy.less( a, b) ),
        ">" : ( lambda a,b: numpy.greater( a, b) ),
        "=" : ( lambda a,b: numpy.equal( a, b) ),
        "!=" : ( lambda a,b: numpy.not_equal( a, b) ),
        "<=" : ( lambda a,b: numpy.less_equal( a, b) ),
        ">=" : ( lambda a,b: numpy.greater_equal( a, b) )
      }

func = { "sin": numpy.sin,
         "asin": numpy.arcsin,
         "cos": numpy.cos,
         "abs": numpy.abs,
         "acos": numpy.arccos,
         "tan": numpy.tan,
         "atan": numpy.arctan,
         "atan2": numpy.arctan2,
         "exp": numpy.exp,
         "ln": MathOperations.lnLim,
         "log": MathOperations.logLim,
         "sqrt": numpy.sqrt,
         "eq": equal,
         "ne": not_equal,
         "lt": less,
         "pow": numpy.power,
         "gt": greater,
         "le": less_equal,
         "ge": greater_equal,
         "ddx": MathOperations.diferentiateLon,
         "ddy": MathOperations.diferentiateLat,
         "intx": MathOperations.integralLon,
         "inty": MathOperations.integralLat,
         "dvg": MathOperations.divergence,
         "intS": MathOperations.surfaceIntegral,
         "intF": MathOperations.integrateFields,
         "ddF": MathOperations.diferentiateFields,
         "min": MathOperations.multimin,
         "max": MathOperations.multimax
       }
p = ""
yes = True

# Expression evaluation using indirect recursion - works with brackets, priority and all
def evaluate(s, row, size, count):
	print s
	global yes
	global p
	if yes:
		p = s.pop()
		yes = False

	r = term(s, row, size, count)
	if len(s)<=0:
		return r
	while len(s)>0 and (p == '+' or p == '-'):
		if p == '+':
			print "Doing Addition"
			p = s.pop()
			r += opn['+'](r, term(s, row, size, count))
			print "Finished Addition"
		elif p == '-':
			p = s.pop()
			print "Entering Subtraction"
			r = opn['-'](r, term(s, row, size, count))
			print "Finished Subtraction"
	return r

def term(s, row, size, count):
	global p
	print "Entering term", p
	r = factor(s, row, size, count)
	if len(s)<=0:
		return r

 	while True:
		p = s.pop() #Get he sign

		if p == '*':
			print "Doing Multiplication"
			p = s.pop() #get the factor
			r = opn["*"](r, factor(s, row, size, count))
			print "Finished Multiplication"
		elif p == '/':
			print "Doing Division"
			p = s.pop() #get the factor
			r = opn["/"](r, factor(s, row, size, count))
			print "Finished Division"
		if not (len(p)>0 and (p == '*' or p == '/')):
			break
	print "Exiting term", p
	return r

def factor(s, row, size, count):
	
	global p
	print "Entering factor", p
	if p == '(':
		print "Open Brackets"
		p = s.pop() #'('
		r = evaluate(s, row, size, count)
		print "Close Brackets"
		return r
	elif p[0]>='0' and p[0]<='9':
		r = float(p)
		return r
	elif p[0]=='[':
		lay = p 
		s.pop() # @
		p = s.pop()
		num = int(p)

		return returnBand( lay, num, row, size, count )
	elif p == "PI":
		return math.pi
	elif p == "E":
		return math.e
	elif p in func:
		if p in [ "eq", "ne", "gt", "lt", "ge", "le" ]:
			op = p
			s.pop() #'('
			p = s.pop() #p is the first argument
			op1 = evaluate(s, row, size, count)
			p = s.pop() #p is the second argument
			op2 = evaluate(s, row, size, count)
			p = s.pop() #p is the third argument
			op3 = evaluate(s, row, size, count)
			r = func[op](op1, op2, op3)
			return r
		if p in ["intF", "ddF", "pow" ]:
			op = p # Retain the function in a variable		
			s.pop() #Go over '('
			p = s.pop() # take the first value
			op1 = evaluate(s, row, size, count) # evaluate it
			p = s.pop()
			op2 = evaluate(s, row, size, count)
			r = func[op](op1, op2)
			return r
		if p in ["min", "max", "log"]:
			op = p
			op1 = []
			rasterListTemp = []
			floatListTemp = []
			floatListIndx = []
			done = False
			s.pop() #Go over '('
			while True:
				p = s.pop() # take the parameter
				x = evaluate(s, row, size, count)
				if not(isinstance(x,float) or isinstance(x,int)): 
					op1.append(x)
					rasterListTemp.append(x)
					if not done:
						for i in range(len(floatListTemp)):
							x = x*numpy.ones_like(rasterListTemp[0])
							op1.insert(floatListIndx[i],floatListTemp)
						done = True
				else:
					if not done:
						floatListIndx.append(len(op1)+len(floatListTemp))
						floatListTemp.append(x)
					else:
						x = x*numpy.ones_like(rasterListTemp[0])
						op1.append(x)
				if p == ')':
					break				
			op1 = numpy.array(op1)
			return func[op](op1)
			
		#Otherwise, it has to be a one argument function:
		op = p # Take the function
		s.pop() #Go over '('
		p = s.pop()
		x = evaluate(s, row, size, count) #evaluate the parameter
		print x
		return func[op](x) 
	print "Exiting factor", p
