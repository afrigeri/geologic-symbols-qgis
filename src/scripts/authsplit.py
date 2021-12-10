#!/Applications/QGIS3.14.app/Contents/MacOS/bin/python3
#!/bin/env python3
#
#
# (c) 2021 - Alessandro Frigeri, Istituto Nazionale di Astrofisica
#
# authsplit - splits qgis xml style file into n xml files containing symbols for each authority specified at command line
# 

import xml.etree.ElementTree as ET
import sys,string

auth = sys.argv[1]
infile = sys.argv[2]
outfile = sys.argv[3]

filename = format( outfile )
f = open(filename, 'wb')
f.write(b"<qgis_style version=1>\n<symbols>\n")

context = ET.iterparse( infile , events=('end','start' ))
depth = 0
for event, elem in context:
    if elem.tag == 'symbol':
        if event == 'end':
           depth -= 1
        if event == 'start':
           depth += 1
        names = elem.get('tags')
        print(names)
        if names:
            names_lst = names.split(',')
            if auth in names_lst:
                name = auth
                if depth == 0: 
                    f.write(ET.tostring(elem))

f.write(b"\n</symbols>")
f.write(b"\n<qgis_style>")
f.close()
