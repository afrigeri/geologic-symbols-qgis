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
from pytablewriter import MarkdownTableWriter

writer = MarkdownTableWriter()
writer.table_name = "Table of symbols"
writer.headers = ["Authority", "code", "description", "notes"]
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

for rootdir, dirs, files in os.walk( srcdir ):    
   for filename in files:
      if filename.endswith(".xml"): 
         xmlfile = os.path.join(rootdir, filename)
         auth = os.path.dirname( xmlfile ).split('/')[-1]
         tree = ET.parse( xmlfile )
         root = tree.getroot()
         if root.findall("./symbols/symbol"):
            for symbol in root.findall("./symbols/symbol"):    
               symbol.attrib['tags'] = auth+',geology'
               n = (symbol.attrib['name'])
               c,d = name_parser( n )
            symbols.append(symbol)
            writer.value_matrix.append([auth,str(c),d,''])
               
         if root.findall("./colorramps/colorramp"):
            colorramps = ET.SubElement(top, 'colorramps')
            for colorramp in root.findall("./colorramps/colorramp"):
               colorramp.attrib['tags'] = auth+',geology'
               n = colorramp.attrib['name']
               c,d = name_parser( n )
            colorramps.append(colorramp)
            writer.value_matrix.append([auth,str(c),d,''])

ElementTree(indent(top)).write(dst)
writer.write_table()
writer.dump("../STATUS.md")
