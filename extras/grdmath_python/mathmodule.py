import os

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

import sys #is this being used?
import copy
import gc

'''
Module to run grdmath in python

Within a Console typical usage would be to assign the filepath of each rastor file used to
an infile() class instance and assign an associate ref.  The same would then be done with
output file locations with the outfile class.  finally run() enables the user to preform
operations on the rastor files using there ref as arguments.  The name of the functions used
are the same as in grdmath but are in the form FUNC(arg1) or FUNC(arg1,arg2).  The result is
outputed to a specified output file location.
'''

class fls(object):
	'''
	Contains the paths of input and output files as strings
	'''
	infs = []
	infref = []
	outfs = []
	outfref = []
	
class infile(fls):
	'''
	Contains a single input file and its associated reference

	The class links a variable name defined as argument ref with
	a filepath for use in the replaceFileVar function.
	
	The ref can be used instead of the filepath when writing 
	python strings for the 'Rastor Function' and the argument
	of python input. 
	'''
	def __init__(self, inputfilename, ref):
		if ".nc" in inputfilename:
			self.var = inputfilename
		else:
			self.var = '%s.nc' %(inputfilename)
		fls.infs += [self.var]
		self.ref = ref
		fls.infref += self.ref

class outfile(fls):
	'''
	Contains a single output file and its associated reference
		
	ref is used to call the file in run() with the string ' ref '
	'''
	def __init__(self, outputfilename, ref):
		if ".nc" in outputfilename:
			self.var = outputfilename
		else:
			self.var = '%s.nc' %(outputfilename)
		fls.outfs += [self.var]
		self.ref = ref
		fls.outfref += self.ref

def pythoninput(x):
	'''
	converts a user input to reverse polish notation

	converts strings in python function form of 'FUNC(a,b)'
	to reverse polish notation of ' b a FUNC' which is used 
	by grdmath
	'''
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


def replaceFileVar(string, flstype = 'infile'):
	'''
	replaces the variables asigned to classes with the filepath

	Acts upon a string and replaces sections of form ' a ' with
	a filepath if 'a' is in an infile.ref
	'''
	if flstype == 'infile':		
		for i in range(len(fls.infref)):						
			a1 = ' '+fls.infref[i]+' '
			b1 = ' '+fls.infs[i]+' '
			string = string.replace(a1,b1)
	else:
		for i in range(len(fls.outfref)):						
				a1 = ' '+fls.outfref[i]+' '
				b1 = ' '+fls.outfs[i]+' '
				string = string.replace(a1,b1)
	return string

def upperCase(grdstring): #still problem with uppercase
	wordlist = grdstring.split()
	for i in wordlist:
		if not('/' in i):
			i = i.upper()
		else:
			i = i
	result = ''
	for i in wordlist:
		result += ' ' + i
	return result

def grdfunc(func, arg1, arg2 = 'empty'):
	'''
	returns a string in reverse polish notation for function func
	'''
	if arg2 == 'empty':
		return ' '+str(arg1)+' '+str(func)
	else:
		return ' '+str(arg1)+' '+str(arg2)+' '+str(func)

def grd_calc(grdstring, resultfile):
	'''
	runs grdmath on grdstring and ouputs to resultfile
	'''
	if not ('.nc' in resultfile):	
		resultfile = '%s.nc' % str(resultfile)
	grdstring = '/usr/lib/gmt/bin/grdmath'+str(grdstring)+' = '+str(resultfile)
	print grdstring
	os.system(grdstring)

def run():
	'''
	User python interface to preform calculations with grdmath

	interprets userinputs as strings and runs them with grdmath.
	User must specify an output file for each result.  Input 
	files which have been assigned as an argument to the infile()
	 class can be called in the 'Rastor Function:' by there ref.  
	Output files simerly assigned can be called using ' ref '.

	To exit type exit into 'Rastor Function:'.
	'''
	running = True
	count = 1
	while running == True:
		commandString = 'Command['+str(count)+']:'
		string = str(raw_input(commandString))
		count += 1
		if string == 'exit':
			break
		elif string == 'input' or string == 'infile':
			try:
				filepath = eval(raw_input('Input File Path:'))
			except:
				print 'Warning: InvalidInput' #redefine properly at some point
				continue
			try:
				ref = eval(raw_input('File referance:'))
			except:
				print 'Warning: InvalidInput'
				continue
			infile(filepath,ref)
		elif string == 'output' or string == 'outfile':
			try:
				filepath = eval(raw_input('Output File Path:'))
			except:
				print 'Warning: InvalidInput'
				continue
			try:
				ref = eval(raw_input('File referance:'))
			except:
				print 'Warning: InvalidInput'
				continue
			outfile(filepath,ref)
		elif string == 'filelist' or string == 'files':
			print 'input file paths: ', fls.infs
			print 'input file references: ', fls.infref
			print 'output file paths: ', fls.outfs
			print 'output file references: ', fls.outfref
		elif string == 'load':
			try:
				filename = eval(raw_input('File to load:'))
			except:
				print 'Warning: InvalidInput'
				continue
			filename = replaceFileVar(filename, outfile)
			osString = 'qgis'+filename
			os.system(str(osString))
		else:
			grdstring = pythoninput(string)
			grdstring = replaceFileVar(grdstring)
			grdstring = upperCase(grdstring)
			try:
				resultfile = eval(raw_input('Output File Name:'))
			except:
				print 'Warning: InvalidInput'
				continue
			resultfile = replaceFileVar(resultfile, outfile)
			if ".nc" in resultfile:
				resultfile = resultfile
			else:
				resultfile = '%s.nc' %(resultfile)
			grd_calc(grdstring, resultfile)

if __name__ == '__main__':
	run()
