prefix = /usr
datadir = $(prefix)/share

plugindir = $(datadir)/qgis/python/plugins/
localplugindir = ${HOME}/.qgis/python/plugins/
testdir = dev/plugins/mesh_netcdf/
DEVPACKAGEFILES = mesh_netcdf  rastercalc  rasterise_polygons define_boundary_ids
PACKAGEFILES = mesh_netcdf  rastercalc  rasterise_polygons Polygonizer QuickMultiAttributeEdit

.PHONY: install
install:
	install -d $(DESTDIR)$(plugindir)
	cp -a $(foreach FILE, $(PACKAGEFILES), release/$(FILE)) $(DESTDIR)$(plugindir)
	chmod a+rX -R $(foreach FILE, $(PACKAGEFILES), release/$(FILE)) $(DESTDIR)$(plugindir)

.PHONY: uninstall
uninstall:
	rm -rf $(foreach FILE, $(PACKAGEFILES), $(DESTDIR)$(plugindir)/$(FILE))

.PHONY: installdev
installdev:
	install -d $(localplugindir)
	cp -a $(foreach FILE, $(DEVPACKAGEFILES), dev/plugins/$(FILE)) $(localplugindir)
	chmod u+rX -R $(foreach FILE, $(DEVPACKAGEFILES), dev/plugins/$(FILE)) $(localplugindir)

.PHONY: test
test: 
	python $(testdir)/generator.py


