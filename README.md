
![QGIS](docs/images/ss01.png)

## Geologic symbols library and development for QGIS 
#### June, 2019


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




