#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
- Here we can audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
- the update_name function, to fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import codecs

OSMFILE = "../data/kyiv_ukraine.osm"

# Note that we must use re.UNICODE key to match unicode strings
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE | re.UNICODE)


expected_en = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

expected_uk = [u"шосе", u"шлях", u"узвіз", u"тупик", u"проїзд", u"проспект", u"провулок", u"площа", u"набережна", u"дорога", u"вулиця",
               u"бульвар", u"алея"]

#mapping_en = { "St": "Street",
#            "St.": "Street",
#            "Rd.": "Road",
#            "Ave": "Avenue"
#            }

# Most of the street names are in Ukrainian
# Only one thing was encountered that must be fixed
mapping_uk = { u'вул.' : u'вулиця' }

'''
Because we use Unicode literals, pprint outputs unicode bytes. 
In order to see the drawn characters we use this class
'''
class UnicodePPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)


def audit_street_type(street_types, street_name, lang):
    m = street_type_re.search(street_name)
    #print type(street_name)
    if m:
        street_type = m.group()

        if lang == "uk":
            if street_type not in expected_uk:
                #print type(street_type)
                #print street_type + "isn't there"
                street_types[street_type].add(street_name)
        elif lang == "en":
            if street_type not in expected_en:
                street_types[street_type].add(street_name)


def is_street_name_uk(elem):
    return (elem.attrib['k'] == "addr:street")

def is_street_name_en(elem):
    return (elem.attrib['k'] == "addr:street:en")


def audit(osmfile):
    #osm_file = codecs.open(osmfile, encoding="utf-8", mode = "r")
    osm_file = codecs.open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":

            for tag in elem.iter("tag"):

                if is_street_name_uk(tag):
                    audit_street_type(street_types, tag.attrib['v'], "uk")

                elif is_street_name_en(tag):
                    audit_street_type(street_types, tag.attrib['v'], "en")

    return street_types


def update_name(name, mapping):
    '''
    Fixes the street names.
    '''
    for key, val in mapping_uk.iteritems():
        street_type_re = re.compile(key, re.IGNORECASE | re.UNICODE)

        m = street_type_re.search(name)

        if m:
            name = re.sub(key, "", name)
            name = name + " " + val
            break

    return name


def test():
    st_types = audit(OSMFILE)
    UnicodePPrinter().pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping_uk)
            print name, "=>", better_name
#            if name == "West Lexington St.":
#                assert better_name == "West Lexington Street"
#            if name == "Baldwin Rd.":
#                assert better_name == "Baldwin Road"
#

if __name__ == '__main__':
    test()
