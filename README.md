
![QGIS](docs/images/ss01.png)

## Geologic symbols library and development for QGIS 
#### Alessandro Frigeri, IAPS/INAF - June, 2019


Here you find symbols for QGIS useful in geological mapping.  At the moment there are symbols defined by FGDC, but others from different mapping authorities/institutionis can be added.

### Installation and setup

1. Download the [zipfile](https://github.com/afrigeri/geologic-symbols-qgis/raw/master/dist/geologic_symbols_qgis.zip) containing the symbology files.
2. Extract the zip archive and move the __svg__ directory to a place where you want to store the patterns and symbols.  It can be any directory.
3. Open QGis and go to 'Settings -> Options' (Ubuntu) or 'Preferences' (OSX) and select the second tab from the top: 'System'
4. Under the __SVG Paths__ form click the add button and select the directory where you moved the __svg__ directory
5. In QGis, go to 'Settings -> Style Manager' and click on 'Import/Export -> Import items' button (at bottom-left)
6. Select the __geologic_symblib.xml__ file you have found in the zip file
7. You should now have the geologic symbols working in your QGis!

### Development of new symbols

You can add new symbols by adding to the src/xml the xml file generated into the Style Manager.

### Usage notes

convention here is to draw features clockwise, so non-symmetric symbology is displayed correctly.


### Similar projects

The problem of having a meaningful symbology in modern softwares has been in the air from a while.  Similarly to this project some other example have been available and are actively creating interesting solutions.

 * [QGis Geologic Symbols project from Ryan Mikulovsky at ucdavis, 2010](http://geo.distortions.net/2010/12/geologic-symbology-for-qgis.html)
 * [Stefan Revets project on SourceForge, 2015-2016](https://sourceforge.net/projects/qgisgeologysymbology/)
 * [FGCD Geologic Patterns for the Web by Daven Quinn, 2017](https://davenquinn.com/projects/geologic-patterns/). This project adopts the FGDC pattern of Daven Quinn, contributed by USGS personnell.

### References

* A. Nass, S. van Gasselt, R. Jaumann, H. Asche, Implementation of cartographic symbols for planetary mapping in geographic information systems, Planetary and Space Science, Volume 59, Issues 11-12, September 2011, Pages 1255-1264, ISSN 0032-0633, http://dx.doi.org/10.1016/j.pss.2010.08.022.
(http://www.sciencedirect.com/science/article/pii/S0032063310002606)

* Naß, A.; Fortezzo, C. M.; Skinner, J. A. Cartographic Symbolization in Geologic and Geomorphologic Maps — Specified Collection and GIS-Based Implementation for Planetary Science.  Third Planetary Data Workshop and The Planetary Geologic Mappers Annual Meeting, held June 12-15, 2017 in Flagstaff, Arizona. LPI Contribution No. 1986, id.7064

* Nass, Andrea; Fortezzo, Corey; Skinner, James, Jr.; Hunter, Marc; Hare, Trent Updated symbol catalogue for geologic and geomorphologic mapping in Planetary Scinces.  19th EGU General Assembly, EGU2017, proceedings from the conference held 23-28 April, 2017 in Vienna, Austria., p.16858
