
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

DESTDIR = /usr/share/qgis/python/plugins/
LOCALDESTDIR = ~/.qgis/python/plugins/

default: test

test:
	@make -s -C examples

install:
	cp -r QGis\ Plugins/{Define_Boundary_Ids,MeshNetCDF,rastercalc,RasterisePolygons} $(DESTDIR)
	chmod a+rx -R $(DESTDIR)/{Define_Boundary_Ids,MeshNetCDF,rastercalc,RasterisePolygons}
	
installlocal:
	cp -r QGis\ Plugins/{Define_Boundary_Ids,MeshNetCDF,rastercalc,RasterisePolygons} $(LOCALDESTDIR)
	chmod u+rx -R $(LOCALDESTDIR)/{Define_Boundary_Ids,MeshNetCDF,rastercalc,RasterisePolygons}

