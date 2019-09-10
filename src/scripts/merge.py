#!/env/python
#
# merge-symbols: merge geologic symbols into a single library. 
#
# (c) 2019 Alessandro Frigeri, Istituto di Astrofisica e Planetologia Spaziali - INAF - Rome
#

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree
import os,sys
from xml.dom import minidom
import glob
from pytablewriter import MarkdownTableWriter, String
import datetime

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPainter
 
import qgis
from qgis.core import (QgsSymbol,
                       QgsFillSymbol,
                       QgsMarkerSymbol,
                       QgsLineSymbol,
                       QgsLimitedRandomColorRamp,
                       QgsStyleModel,
                       QgsStyle,
                       QgsStyleProxyModel,
                       QgsTextFormat,
                       QgsPalLayerSettings,
                       QgsWkbTypes)

from qgis.testing import start_app

start_app()

writer = MarkdownTableWriter()
status_header = "# Table of symbols, updated "+datetime.date.today().strftime("%B %d, %Y")+"\n"
writer.table_name = ""
writer.headers = ["graphics","authority", "code", "description", "notes"]
writer.type_hints = [String,String,String,String,String]
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
    name convention:
    
    [name or id] : [ description ]
    '''
    return name.split(':')

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
            writer.value_matrix.append([ lnk ,auth,str(c),d,''])

               
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
