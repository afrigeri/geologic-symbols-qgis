#!/Applications/QGIS3.14.app/Contents/MacOS/bin/python3
# 
# Usage of @executable_path is the limitation of the current all-in-one MacOS QGIS bundle.
# see https://wincent.com/wiki/@executable_path,_@load_path_and_@rpath 
# pip3 install --prefix=/Applications/QGIS3.14.app/Contents/Resources/python/ package_name
# 
# merge-symbols: merge geologic symbols into a single library. 
#
# (c) 2019-2021 Alessandro Frigeri, Istituto di Astrofisica e Planetologia Spaziali - INAF - Rome
#
# it's critical to:
# export QT_QPA_PLATFORM_PLUGIN_PATH=/Applications/QGIS3.10.app/Contents/PlugIns/

import os, sys
#sys.path.insert(0, "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/")
#sys.path.append("/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/")

import logging as log

log.basicConfig(filename="merge.log",
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=log.INFO)

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree
from xml.dom import minidom
import glob

#import pytablewriter
#from pytablewriter import MarkdownTableWriter

from scripts.md_writer import MyMarkdownTableWriter as MarkdownTableWriter

import datetime

from validation import *


from PyQt5.QtCore import QSize, QSettings
from PyQt5.QtGui import QImage, QPainter
 
import qgis

#from qgis.core import (QgsSymbol,
#                       QgsFillSymbol,
#                       QgsMarkerSymbol,
#                       QgsLineSymbol,
#                       QgsLimitedRandomColorRamp,
#                       QgsStyleModel,
#                       QgsStyle,
#                       QgsStyleProxyModel,
#                       QgsTextFormat,
#                       QgsPalLayerSettings,
#                       QgsWkbTypes)

from qgis.core import *

# Supply path to qgis install location

if sys.platform == "darwin":
	# /Applications/QGIS3.10.app/Contents/MacOS/
    QgsApplication.setPrefixPath("/Applications/QGIS.app/Contents/MacOS/", True)
elif sys.platform == "linux":
    QgsApplication.setPrefixPath("/usr/", True)
elif sys.platform == "win32":
    QgsApplication.setPrefixPath("C:/Program Files/QGIS 3.10", True) 


#svg_paths = QSettings().value('svg/searchPathsForSVG')
#print(svg_paths)
#svg_paths.append('./svg')
#QSettings().setValue('svg/searchPathsForSVG', svg_paths)



SVG_DIR="gsymblib-svg"

#from qgis.testing import start_app
# QGISAPP = start_app()
# Create a reference to the QgsApplication.  
QGISAPP = QgsApplication([], False)

# Load providers
# QGISAPP.initQgis()


svgpaths = QGISAPP.svgPaths()
svgpaths.append('.%s/'%SVG_DIR)
svgpaths.append( os.path.join( os.getcwd(), SVG_DIR ) ) 
QGISAPP.setDefaultSvgPaths(svgpaths)
print(QGISAPP.svgPaths())

import locale
#locale.setlocale(locale.LC_TIME, "en_US.utf8") # date in english
locale.setlocale(locale.LC_TIME, "en_US.UTF-8")

writer = MarkdownTableWriter()
status_header = "# Gsymblib symbols list, updated "+datetime.date.today().strftime("%B %d, %Y")+"\n"
writer.table_name = ""
writer.headers = ["graphics","authority", "code", "description", "notes"]
#writer.type_hints = [pytablewriter.String, pytablewriter.String, pytablewriter.String, pytablewriter.String, pytablewriter.String]
writer.value_matrix = []

def indent(elem, level=0):
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem

def name_parser(name):
    '''
    symbol's name convention:
    [name or id] : [ description ]
    
    ":" is mandatory
    
    '''
    try:
        a, b = name.split(':')
    except:
        print("The symbol name \" %s \" does not follow the gsymlib naming convention"%name)
        sys.exit(0)
		
    return a.strip(), b.strip()

srcdir = sys.argv[1]
dst = sys.argv[2] 

top = ET.Element('qgis_style', version="1")
comment = ET.Comment('geologic symbols for QGis')
top.append(comment)

symbols = ET.SubElement(top, 'symbols')

count_dict = {}

status_file  = open('../STATUS.md','w') 

for rootdir, dirs, files in os.walk( srcdir ):    
   for filename in files:
      if filename.endswith(".xml"): 
         xmlfile = os.path.join(rootdir, filename)
         auth = os.path.dirname( xmlfile ).split('/')[-1]
         
         #if n_styles != 1:
         #   print("xml should contain just one symbol")
         #   print("{} contains {}".format(xmlfile,n_styles))
         #   sys.exit(0)


         if auth not in count_dict.keys():
            count_dict[auth] = 0
         tree = ET.parse( xmlfile )
         root = tree.getroot()

         #if not validate_and_clean_xml(root,filename=extract_name(filename)):
         #    log.error(f"cannot validate {filename}")

         if root.findall("./symbols/symbol"):
            for symbol in root.findall("./symbols/symbol"):    
               symbol.attrib['tags'] = auth+',geology'
               n = (symbol.attrib['name'])
               print(n)
               c,d = name_parser( n )
            symbols.append(symbol)
            count_dict[auth] += 1
            

            style = QgsStyle()
            style.importXml( xmlfile )
            n_styles = style.symbolCount()
            symbol_name = style.symbolNames()[0]
            symbol = style.symbol(symbol_name)
            size = QSize(64, 64)
            image = symbol.asImage(size)
            path, filename = os.path.split( xmlfile )
            png_filename = filename.replace('.xml','.png')
            png_dir = os.path.join("../docs/images/library/",auth)

            if not os.path.exists( png_dir ):
               os.makedirs( png_dir )
            image.save(r"{}".format(png_dir+'/'+png_filename), "PNG")
            
            status_path = os.path.join("docs/images/library/",auth)
            lnk = "![]({})".format( os.path.join( status_path, png_filename ))
            writer.value_matrix.append([ lnk ,auth,str(c), d ,''])

               
         if root.findall("./colorramps/colorramp"):
            colorramps = ET.SubElement(top, 'colorramps')
            for colorramp in root.findall("./colorramps/colorramp"):
               colorramp.attrib['tags'] = auth+',geology'
               n = colorramp.attrib['name']
               c,d = name_parser( n )
            colorramps.append(colorramp)
            count_dict[auth] += 1
            writer.value_matrix.append([auth,str(c),d,''])

ElementTree(indent(top)).write(dst)
writer.value_matrix.sort()
writer.write_table()
status_file.write(status_header)
status_file.write("There are:\n")    
for k in count_dict.keys():
    status_file.write(" * %d entries for %s.\n"%(count_dict[k],k))    
status_file.write("\n")    

status_file.write(writer.dumps()) 
status_file.close()
print(count_dict)

# Finally, exitQgis() is called to remove the
# provider and layer registries from memory
QGISAPP.exitQgis()

