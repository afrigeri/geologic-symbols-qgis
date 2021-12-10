#
# Copyright (C) 2019-2021 Alessandro Frigeri, Istituto di Astrofisica e Planetologia Spaziali
# 
# Geologic symbols in qgis.
#
# 
# set
# export PYTHONPATH=/<qgispath>/Contents/Resources/python

# OSX
#
UNAME := $(shell uname)

PYTHON=python3
ifeq ($(UNAME), Darwin)
PYTHON=/Applications/QGIS3.10.app/Contents/MacOS/bin/python3 
# QGIS dev in OSX brings to segfault
#PYTHON=/Applications/QGIS.app/Contents/MacOS/bin/python3
endif
ifeq ($(UNAME), Linux)
PYTHON=python3.8
endif

SRC_DIR := xml

REPO_DIR := ..
DIST_DIR := $(REPO_DIR)/dist
DIST_VERSION := 1.0.0
PACKAGE_NAME := gsymblib-$(DIST_VERSION)
PACKAGE_DIR := $(DIST_DIR)/$(PACKAGE_NAME)
TARGET_XML := gsymblib-$(DIST_VERSION).xml
TARGET := $(DIST_DIR)/$(TARGET_XML)
HANDOUT_PDF := $(PACKAGE_NAME)-handout.pdf

# COLLECTIONS (QGIS RESOURCE MANAGER PLUGIN)
COLL_DIR := $(REPO_DIR)/collections
COLL_AUTHS := fgdc
COLL_SVG_DIR := $(COLL_DIR)/svg
COLL_SYM_DIR := $(COLL_DIR)/symbol

SVG_DIR := gsymblib-svg

# These are the file being ditributed into the zip archive
DIST_FILES := $(SVG_DIR) $(DIST_DIR)/$(TARGET_XML) $(DIST_DIR)/$(HANDOUT_PDF) LICENSE.txt

DOCS_DIR := ../docs
ICONS_DIR := $(DOCS_DIR)/images/library

$(TARGET): $(SRC_DIR)
	mkdir -p $(DIST_DIR)
	$(PYTHON) scripts/merge.py $< $@
	make handout

all:
	make update_usgs_patterns
	make $(TARGET)

all_nonet: clean
	make $(TARGET)

clean:
	-rm $(TARGET)

dist: clean distclean all
	mkdir -p $(PACKAGE_DIR)
	cp -r $(DIST_FILES) $(PACKAGE_DIR)
	cd $(DIST_DIR); zip -r $(PACKAGE_NAME).zip $(PACKAGE_NAME)/$(TARGET_XML) $(PACKAGE_NAME)/$(SVG_DIR) $(PACKAGE_NAME)/$(HANDOUT_PDF) $(PACKAGE_NAME)/LICENSE.txt
	#cd $(DIST_DIR); cp $(TARGET_XML) $(COLL_SYM_DIR)
	#cd $(DIST_DIR); cp $(SVG_DIR) $(COLL_XML_DIR)
	#cd $(DIST_DIR); cp $(PACKAGE_NAME)/$(HANDOUT_PDF) $(HANDOUT_PDF)
	rm -rf $(PACKAGE_DIR)

collection_dirs: 
	mkdir -p $(COLL_DIR)/fgdc
	mkdir -p $(COLL_DIR)/fgdc/svg
	mkdir -p $(COLL_DIR)/fgdc/symbol

resmanager: collection_dirs
	python scripts/authsplit.py fgdc $(TARGET) $(COLL_DIR)/fgdc/symbol/fgdc.xml
	cp -r gsymblib-svg/patterns/fgdc $(COLL_DIR)/fgdc/svg

distclean:
	-rm -rf $(PACKAGE_DIR)
	-rm $(DIST_DIR)/$(PACKAGE_NAME).zip

handout:
	cd $(REPO_DIR); pandoc --variable mainfont="Helvetica" --variable sansfont="Helvetica" --variable monofont="Menlo" --variable fontsize=10pt  -V geometry:margin=1cm --pdf-engine xelatex STATUS.md -o dist/$(HANDOUT_PDF)

manual:
	cd ../docs/; make latexpdf

# We must convert all to SVG Tiny
# https://github.com/manisandro/svg2svgt
update_usgs_patterns:
	svn export --force https://github.com/davenquinn/geologic-patterns/trunk/assets/svg $(SVG_DIR)/patterns/fgdc
	# Convert svg to svg Tiny 1.2 which is required by Qt5
	for svgfile in $(shell ls $(SVG_DIR)/patterns/fgdc/*.svg) ; do \
    		svg2svgt $${svgfile} $${svgfile}.tiny ; \
		mv $${svgfile}.tiny.svg $${svgfile} ; \
	done

