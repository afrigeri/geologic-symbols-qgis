#
# Copyright (C) 2019 Alessandro Frigeri, Istituto di Astrofisica e Planetologia Spaziali
# 
# Geologic symbols in qgis.
#
# 


SRC_DIR := xml

DIST_DIR := ../dist
PACKAGE_NAME := geologic_symbols_qgis
PACKAGE_DIR := $(DIST_DIR)/$(PACKAGE_NAME)
TARGET_XML := geologic_symblib.xml
TARGET := $(DIST_DIR)/$(TARGET_XML)

DIST_FILES := svg $(DIST_DIR)/$(TARGET_XML)

$(TARGET): $(SRC_DIR)
	mkdir -p $(DIST_DIR)
	python scripts/merge.py $< $@

all:
	make $(TARGET)

clean:
	-rm $(TARGET)

dist: clean distclean all
	mkdir -p $(PACKAGE_DIR)
	cp -r $(DIST_FILES) $(PACKAGE_DIR)
	cd $(DIST_DIR); zip -r $(PACKAGE_NAME).zip $(PACKAGE_NAME)/$(TARGET_XML) $(PACKAGE_NAME)/svg
	rm -rf $(PACKAGE_DIR)

distclean:
	-rm -rf $(PACKAGE_DIR)
	-rm $(DIST_DIR)/$(PACKAGE_NAME).zip

update_usgs_patterns:
	svn export --force https://github.com/davenquinn/geologic-patterns/trunk/assets/svg svg/patterns/fgcd
