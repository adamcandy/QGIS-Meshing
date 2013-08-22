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

