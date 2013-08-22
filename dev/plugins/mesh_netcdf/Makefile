# Makefile for Define Boundary Ids plugin 
UI_FILES = ui_meshnetcdf.py

RESOURCE_FILES = resources.py

default: compile
	
compile: $(UI_FILES) $(RESOURCE_FILES)

%.py : %.qrc
	pyrcc4 -o $@  $<

%.py : %.ui
	pyuic4 -o $@ $<

clean:
	rm -f $(UI_FILES) $(RESOURCE_FILES)
