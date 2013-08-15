prefix = /usr
datadir = $(prefix)/share

plugindir = $(datadir)/qgis/python/plugins/
localplugindir = ${HOME}/.qgis/python/plugins/
DEVPACKAGEFILES = mesh_surface  meshing_raster_calc  rasterise_polygons boundary_identification
PACKAGEFILES = mesh_surface  meshing_raster_calc  rasterise_polygons Polygonizer QuickMultiAttributeEdit

testdir = ./plugins/mesh_netcdf/
outputdir = ./tests/output/

.PHONY: install uninstall installdev test clean

install:
	install -d $(DESTDIR)$(plugindir)
	cp -a $(foreach FILE, $(PACKAGEFILES), release/$(FILE)) $(DESTDIR)$(plugindir)
	chmod a+rX -R $(foreach FILE, $(PACKAGEFILES), release/$(FILE)) $(DESTDIR)$(plugindir)

uninstall:
	rm -rf $(foreach FILE, $(PACKAGEFILES), $(DESTDIR)$(plugindir)/$(FILE))

installdev:
	install -d $(localplugindir)
	cp -a $(foreach FILE, $(DEVPACKAGEFILES), plugins/$(FILE)) $(localplugindir)
	chmod u+rX -R $(foreach FILE, $(DEVPACKAGEFILES), plugins/$(FILE)) $(localplugindir)

clean:
	rm -rf $(outputdir)

test: clean 
	#python $(testdir)/generator.py
	python $(testdir)/modular_generator.py
	

