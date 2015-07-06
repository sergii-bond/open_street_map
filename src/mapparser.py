#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Here we use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
"""
import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    osm_file = open(filename, "r")

    d = {}
    for event, elem in ET.iterparse(osm_file):
        if elem.tag not in d:
            d[elem.tag] = 1
        else:
            d[elem.tag] += 1

    return d


def test():

    tags = count_tags('../data/kyiv_ukraine.osm')
    pprint.pprint(tags)
    

if __name__ == "__main__":
    test()
