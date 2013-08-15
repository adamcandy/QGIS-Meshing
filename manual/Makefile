
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

ROOT_TEX_FILE=meshing_manual.tex
bib_file=meshing_manual.bib
ALL_TEX_FILES=$(wildcard */*.tex) $(wildcard *.tex)
IMAGE_DIRS=meshing_images

#VERSION = $(shell ../bin/version-info | tr -d [:punct:]) 
#VERSION = $(bzr revno) 
VERSION = 1
ROOT_PDF_FILE=$(patsubst  %.tex, %.pdf, $(ROOT_TEX_FILE))
XFIG_IMAGES=$(wildcard $(IMAGE_DIRS)/*/*.fig)
PDF_IMAGES=$(wildcard $(IMAGE_DIRS)/*/*.pdf)
EPS_IMAGES=$(wildcard $(IMAGE_DIRS)/*/*.eps)
SVG_IMAGES=$(wildcard $(IMAGE_DIRS)/*/*.svg)

$(ROOT_PDF_FILE): $(ALL_TEX_FILES) \
	$(XFIG_IMAGES) \
	$(PDF_IMAGES)  \
	$(SVG_IMAGES)  \
	$(EPS_IMAGES)
	#echo $(VERSION) >version.tex
	@echo "(not available)" >version.tex
	@$(MAKE) -C $(IMAGE_DIRS)/ all
	if [ -e ../../.bzr/branch/last-revision ]; then sed -e 's/ .*//' ../../.bzr/branch/last-revision >version.tex; fi
	pdflatex -shell-escape $(ROOT_TEX_FILE)
	if fgrep "Rerun to" meshing_manual.log; then $(MAKE) --assume-new $< $@;fi
ifndef NOBIBTEX
	if fgrep "There were undefined"  meshing_manual.log;\
	then bibtex meshing_manual; \
	$(MAKE) NOBIBTEX=true --assume-new $< $@;fi
endif

#linear_1d_mesh.png: linear_1d_mesh.fig

#%.tex: %.pstex_t %.pstex
#	../femtools/doc/bin/wrap_pstex $<

%.dvi: %.tex 
	pdflatex -output-directory $(dir $@) -shell-escape -output-format dvi $<

%.png: %.dvi
	dvipng -T tight  -D 100 -bg Transparent $<  -o $@

%.ps: %.dvi
	dvips -o $@ $^ 

%.pdf: %.tex
	pdflatex -shell-escape $<
	makeindex -s index.ist $(basename $<)
	if fgrep "Rerun to" $*.log; then $(MAKE) --assume-new $< $@;fi
ifndef NOBIBTEX
	if fgrep "There were undefined"  $*.log;\
	then bibtex $*; \
	$(MAKE) NOBIBTEX=true --assume-new $< $@;fi
endif


%.pdftex: %.fig
	fig2dev -L pdftex $^ $@

%_tex.pdf: %.fig
	fig2dev -L pdftex $^ $@

%.pdftex_t: %.fig
	fig2dev -L pdftex_t -p $*_tex.pdf $^ $@

%.pstex: %.fig
	fig2dev -L pstex $^ $@

%.pstex_t: %.fig
	fig2dev -L pstex_t -p $*.pstex $^ $@

%.pdf: %.fig
	fig2dev -L pdf $^ $@

#%.png: %.fig
#	fig2dev -L png $^ $@

.PHONY: clean

clean: htclean_meshing_manual
	rm -r $(ROOT_PDF_FILE) *.dvi *.aux */*.aux *.log *.bbl *.blg *.brf *.toc *.lof \
*.idx *.ind *.ilg *.out version.tex meshing_manual-fig* tmp.inputs \
meshing_manual*.png cmsy*.png 2>/dev/null||true
	@$(MAKE) -C $(IMAGE_DIRS)/ clean

htclean_%:
	rm -r $*.4ct $*.4tc $*.css $*.idv $*.lg $*.tmp $*.xref *.html 2>/dev/null||true

bzrclean:
	bzr rm version.tex tmp.inputs meshing_manual.pdf meshing_manual.out meshing_manual.log meshing_manual.idx meshing_manual.aux meshing.aux


