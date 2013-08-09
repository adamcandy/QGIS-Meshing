#! /bin/python

'''
USAGE
call using: python <filepath to mesh_terminal>/mesh_terminal [commands] <DomainFile> <IdFile> <MeshmetricFile>
'''

import sys
import shlex
from scripts import define_id, export_geo
from scripts.MeshOperations import MeshOp
from scripts.PosFileConverter import *
import os
from scripts.flat_mesh_to_spherical import flat_mesh_spherical
import subprocess

class _baseCommands( object ):
	def _usage( self ):
		print '''
		USAGE
		call using: python <filepath to mesh_terminal>/mesh_terminal [COMMANDS] <DomainFile> <IdFile> <Meshmetric>

		enables mesh_netcdf functionality in terminal. Including both geofile,
		shapefile and meshfile manipulation with the option of mesh metrics based
		on netcdf files.

		COMMANDS
		-h	--help		:Displays this message
			--id		:sets the shapefile used for boundary ids
			--defid		:sets the default id
		-m	--metric	:sets the netcdf used as the mesh metric
		-t	--threshold	:filters the domain for island area in km^2
		-g	--geo		:uses a geofile as a domain instead of a shapefile
			--mesh		:calls gmsh for meshing
		-c	--coord		:sets the coordinate space for meshing use:
						F for flat
						L for lonlat projection to sphere
						S for stereographic
						defaults to flat
		-s	--show		:sets the gmsh call for showing mesh/geo
		-l	--line		:sets the line type used when writing the geofile:
						LN for lines with compound lines disabled
						LY for lines with compound lines enabled
						BN for BSplines with compound lines disabled
						BY for BSplines with compound lines enabled
			--mval		:sets a math eval field
		-e			:Shows all errors found after command.
		'''

class Modular_meshing ( define_id.DefineDomain, _baseCommands, MeshOp ):

	domainShapefileLayerFileName = None
	threshold = None
	idFilePath = None
	isIdLayer = False
	geofilepath = None
	singleNetCDFLayerFileName = None
	postviewFileName = None
	compound_line_enable = False
	gmshcall = False
	gmshShow = False
	defID = 0
	coord = 'F'
	BSpline = True
	Compound = False
	mEval = None
	errorHide = True

	commands = {
	'-h':'self._usage()',
	'--help':'self._usage()',
	'--id':'self.get_id()',
	'--defid':'self.set_defid()',
	'--metric':'self.get_metric()',
	'-m':'self.get_metric()',
	'--threshold':'self.set_threshold()',
	'-t':'self.set_threshold()',
	'--geo':'self.set_geo()',
	'-g':'self.set_geo()',
	'--mesh':'self.call_gmsh()',
	'--coord':'self.set_cspace()',
	'-c':'self.set_cspace()',
	'-s':'self.set_gmshShow()',
	'--show':'self.set_gmshShow()',
	'-l':'self.set_lineType()',
	'--line':'self.set_lineType()',
	'--mval':'self.set_mevalcall()',
	'-e':'self.error_explicit()'
	}

	lineType = {
	'LN':'self.BSpline = False; self.Compound = False',
	'LY':'self.BSpline = False; self.Compound = True',
	'BN':'self.BSpline = True; self.Compound = False',
	'BY':'self.BSpline = True; self.Compound = True',
	}

#note compound lines are not being written are bsplines?

#os.system("python "+pwd+"/mesh_terminal --line LY -g "+test+"/test_annulus_LY.geo "+data+"/annulus.shp --mesh --mval 10")

	def __init__( self , commands):
		self.sarg = shlex.split(commands)
		#self.sarg = arguments[1:]
		self.read_sarg()

		#print self.sarg


		if self.domainShapefileLayerFileName != None:
			self.define_bounds(self.isIdLayer)
			self.data = [self.domainData.regionIDs,self.domainData.shapes,self.boundaryIDList,self.domainData.points]
			if self.geofilepath == None:
				self.geofilepath = '%s_idBoundary.geo' % self.domainShapefileLayerFileName[:-4]
			self.export_geo()
			if self.mEval != None:
				self.write_meval()
			if self.postviewFileName != None:
				self.geoFileName = self.geofilepath
				self.gradeToNCFlat()
		if self.gmshcall:
			#os.system('gmsh -2 '+str(self.geofilepath))

			open(os.path.dirname(os.path.realpath(__file__)) + "/output.log", "w").close()

			with open(os.path.dirname(os.path.realpath(__file__)) + "/output.log", "a") as log:
				subprocess.Popen('gmsh ' +str(self.geofilepath) + ' -2', stderr=subprocess.STDOUT, stdout=log, shell=True)

			meshpath = self.geofilepath[:-3] + 'msh'
			if self.coord == 'L' or self.coord == 'S':
				print "Projecting to Sphere..."
				meshpath = flat_mesh_spherical(meshpath,self.coord == 'S')
				print "Mesh Projected."
			if self.gmshShow: #this is not currently working
				#os.system('gmsh ' +str(meshpath))

				open(os.path.dirname(os.path.realpath(__file__)) + "/output.log", "w").close()
				with open(os.path.dirname(os.path.realpath(__file__)) + "/output.log", "a") as log:
					subprocess.Popen('gmsh ' +str(meshpath), stderr=subprocess.STDOUT, stdout=log, shell=True)
		else:
			if self.gmshShow:
				#os.system('gmsh ' +str(self.geofilepath))
				open(os.path.dirname(os.path.realpath(__file__)) + "/output.log", "w").close()
				with open(os.path.dirname(os.path.realpath(__file__)) + "/output.log", "a") as log:
					subprocess.Popen('gmsh ' +str(self.geofilepath), stderr=subprocess.STDOUT, stdout=log, shell=True)



	def read_sarg( self):
		while self.sarg:
			carg = self.sarg.pop(0)
			if '.shp' in carg and self.domainShapefileLayerFileName == None:
				self.domainShapefileLayerFileName = carg
			elif '.nc' in carg:
				self.singleNetCDFLayerFileName = carg
				self.postviewFileName = carg[:-2]+'pos'
				converter.writePosFile(self)
			else:
				if self.errorHide:
					try:
						eval(self.commands[carg])
					except:
					#print 'Incorrect Terminal Commands'
					#self._usage()
						print 'Warning:  Incorrect Terminal Commands. Failure at %s.' % carg
				else:
					eval(self.commands[carg])


	def get_metric( self ):
		self.singleNetCDFLayerFileName = self.sarg.pop(0)
		self.postviewFileName = self.singleNetCDFLayerFileName[:-2]+'pos'
		converter.writePosFile(self)
	def get_id( self ):
		self.idFilePath = self.sarg.pop(0)
		self.isIdLayer = True
	def set_threshold( self ):
		self.threshold = self.sarg.pop(0)
	def call_gmsh( self ):
		self.gmshcall = True
		if self.sarg[0] == 'True' or self.sarg[0] == 'False':
			self.set_gmshShow()
	def set_cspace( self ):
		self.coord = self.sarg.pop(0)
	def set_geo( self ):
		self.geofilepath = self.sarg.pop(0)
	def _usage( self ):
		_baseCommands._usage(self)
	def export_geo( self ):
		export_geo.write_geo_file(self.geofilepath,self.data,self.Compound,self.BSpline)
	def define_bounds( self, isIdLayer ):
		define_id.DefineDomain.define_bounds(self,isIdLayer)
	def set_defid( self ):
		defID = self.sarg.pop(0)
	def set_gmshShow( self ):
		self.gmshShow = self.sarg.pop(0)
	def set_lineType( self ):
		exec(self.lineType[self.sarg.pop(0)])
	def gradeToNCFlat( self ):
		MeshOp.gradeToNCFlat(self)
	def set_mevalcall( self ):
		self.mEval = int(self.sarg.pop(0))
	def write_meval( self ):
		geoFile = open(str(self.geofilepath), 'a')
		geoFile.write('\n//Code added by Mesh NetCDF to create uniform mesh.\n')
		geoFile.write("Field[1] = MathEval;\n")
		geoFile.write('Field[1].F = "%i";\n' % (self.mEval))
		geoFile.write("Background Field = 1;\n")
		geoFile.write("Mesh.CharacteristicLengthExtendFromBoundary = 0;\n")
		geoFile.close()
	def error_explicit( self ):
		self.errorHide = False


#_mainObject()
