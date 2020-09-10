#!/Applications/QGIS3.14.app/Contents/MacOS/bin/python3
#!/bin/env python3
#
#
# (c) 2020 - Alessandro Frigeri, Istituto Nazionale di Astrofisica
#
# symbolsplitter - splits qgis xml style file into n xml files containing one symbol each
# 

import xml.etree.ElementTree as ET
import sys,string

infile = sys.argv[1]

context = ET.iterparse( infile , events=('end','start' ))
depth = 0
for event, elem in context:
    if elem.tag == 'symbol':
        if event == 'end':
           depth -= 1
        if event == 'start':
           depth += 1
        name = elem.get('name')
        if depth == 0: 
            filename = format(name.split(':')[0] + ".xml" )
            with open(filename, 'wb') as f:
               #f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
               f.write(b"<qgis_style version=1>\n<symbols>\n")
               f.write(ET.tostring(elem))
               f.write(b"\n</symbols>")
