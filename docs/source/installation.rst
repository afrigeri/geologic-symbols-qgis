------------
Installation
------------


To install the geologic symbol library you need to download the zipfile of the current distribution, which is available at the github project's page: http://www.github.com/afrigeri/geologic-symbols-qgis.

Once you have the geologic_symblib.zip, decompress it in a directory of your choice.  

For example, if you are running a Mac OSX, you can extract the contents of the zipfile into a folder called __foo__.

Within the __foo__ directory you will find:

 1. an xml file called geologic_symblib.xml, which is the symbol library
 2. a folder called svg, which contains svg graphics and patterns

Now we can configure QGIS to use the symbol library.

First we tell QGIS where to look for SVG pattern and graphics.  In the main program go to 'Settings -> Options', if you have Linux, or 'Preferences' if you run on OSX.  From the panel, select the second tab from the top: 'System'.

In the 'SVG Paths' form, click on the '+' button and select the __foo__ directory where the svg folder  and xml file are located.

Then got to the main QGIS menu and open the 'Style Manager' window from the 'Settings' menu.

At the bottom left of the 'Style Manager' click on 'Import/Export' button and then 'Import items'.  Now select the geologic_symblib.xml file. 
 
You should now have the geologic symbol library available in QGIS.  From the Style Manager you can select all the symbols or only a sub-group of them.  For example, you can select only the FGDC symbols by clicking on the fgdc tag on the left part of the Style Manager.

