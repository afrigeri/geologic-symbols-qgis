import os

import numpy as np

import logging as log



def extract_name(fullname):
    fname = os.path.split(fullname)[-1][:-4]
    return fname


def load_xml(file):
    if not os.path.isfile(file):
        log.error(f"no file at {txml}")
    try:
        root = ET.parse(file).getroot()
        return root
    except Exception as e:
        log.error(f"problem parsing {file}")
        raise (e)

def clean_desc(string):
    return string.split("@")[0]

def clean_code(string):
    return string.split("@")[-1]


def validate_and_clean_xml(root, svgdir=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../svg/")), filename=None):
    """
    simple qgis style additional validation / cleaning -  cleaning not yet implemented for now
    :param xmlfile: the input
    :return: True or False, raise exceptions.
    """
    symbols_elements = list(root.iter('symbol'))
    if len(symbols_elements) == 0:
        log.error(f"{filename} no symbols found, check aborted.")
        return False

    codes = []
    descs = []
    for symbol in symbols_elements:
        name = symbol.get("name")
        try:
            code, desc = name.split(":")
            code = clean_code(code)
            desc = clean_desc(desc)
        except:
            log.error(f"filename {filename}: Cannot split name, missing \":\" ? in {name}. check naming inside xml")

        codes.append(code)
        descs.append(desc)

    if 1:  # Useful maybe (?)
        codes = np.array(codes)  # use use some utils from numpy
        descs = np.array(descs)
        if (not np.all(codes[0] == codes)):
            log.warning(f"filename {filename}: seems in the xml the codes differ {codes}")

        if (not np.all(descs[0] == descs)):
            log.warning(f"filename {filename}: seems in the xml the descriptions differ {descs}")

    code = codes[0]
    desc = descs[0]

    if filename is not None:
        if (code != filename):
            log.error(f"filename {filename}: filename {filename} and code {code} mismatch")

    sdesc = desc.strip().split("@")[0]
    log.debug(f"filename {filename}: working on ID {code}, {sdesc}")

    if "\n" in desc:
        log.warning(f"filename {filename}: description contains newline char.")

    import re
    svgpattern = ".*\.svg"
    allp = list(root.iter('prop'))
    svgs = []
    for prop in allp:
        v = prop.get("v")
        if re.match(svgpattern, v):
            svgs.append(v)

    for svg in svgs:
        fpath = os.path.join(svgdir, svg)
        if not os.path.isfile(fpath):
            log.warning(f"filename {filename}: xml referencing to missing svg at {svg}, expected at full path {fpath}")

    return True
