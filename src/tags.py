#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict
from collections import OrderedDict
"""
Here we  explore the data a bit more.
We check the "k" value for each "<tag>" and see if they can be valid keys in MongoDB,
as well as see if there are any other potential problems.
"""


#Keys that contain letters or undersore only
lower = re.compile(r'^([a-z]|_)*$')
#Keys that consist of two words separated by one semicolon
lower_1_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
#Keys that consist of three words separated by two semicolons
lower_2_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*:([a-z]|_)*$')
#Keys that have at least one character that may designate there is a problem with this key
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

unique_keys = defaultdict(int)
other_keys = defaultdict(int)

def key_type(element, keys):

    if element.tag == "tag":

        k = element.attrib["k"]
        flag = 0

        if re.search(lower, k):
            keys["lower"] += 1
            flag = 1

        if re.search(lower_1_colon, k):
            keys["lower_1_colon"] += 1
            flag = 1

        if re.search(lower_2_colon, k):
            keys["lower_2_colon"] += 1
            flag = 1

        if re.search(problemchars, k):
            keys["problemchars"] += 1
            flag = 1

        if flag == 0:
            other_keys[k] += 1
            keys["other"] += 1

        unique_keys[k] += 1
        
    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_1_colon": 0, "lower_2_colon": 0, "problemchars": 0, "other": 0}

    #for _, element in ET.iterparse(filename, events = ("start", )):
    for _, element in ET.iterparse(filename):
        #for tag in element.iter("tag"): 
        keys = key_type(element, keys)

    unique_keys_ordered = OrderedDict(sorted(unique_keys.items()))
    with open("unique_keys", "w") as f:
        for key, val in unique_keys_ordered.iteritems():
            f.write(key + '   ' + str(val)  + '\n')

    other_keys_ordered = OrderedDict(sorted(other_keys.items()))
    with open("other_keys", "w") as f:
        for key, val in other_keys_ordered.iteritems():
            f.write(key + '   ' + str(val)  + '\n')

    return keys



def test():
    keys = process_map('../data/kyiv_ukraine.osm')
    pprint.pprint(keys)


if __name__ == "__main__":
    test()
