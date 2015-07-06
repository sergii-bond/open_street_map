#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from collections import defaultdict
from collections import OrderedDict
import time
"""
Using this code we Wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"addr": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

For transformations that take place here, please check project documentation
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_1_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
lower_2_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*:([a-z]|_)*$')
lower_3_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*:([a-z]|_)*:([a-z]|_)*$')
mixed = re.compile(r'^([a-z]|[A-z]|_|[0-9]|-)*$')
mixed_1_colon = re.compile(r'^([a-z]|[A-z]|_|[0-9]|-)*:([a-z]|[A-z]|_|[0-9]|-)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

ignored_keys = defaultdict(int)

# Most of the street names are in Ukrainian
# Only one thing was encountered that must be fixed
mapping_uk = { u'вул.' : u'вулиця' }

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

def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        node["type"] = element.tag
        if "id" in element.attrib:
            node["id"] = element.attrib["id"]

        if "visible" in element.attrib:
            node["visible"] = element.attrib["visible"]

        node["created"] = {}
        node["created"]["version"] = element.attrib["version"]
        node["created"]["changeset"] = element.attrib["changeset"]
        node["created"]["timestamp"] = element.attrib["timestamp"]

        if "user" in element.attrib:
            node["created"]["user"] = element.attrib["user"]
        else:
            node["created"]["user"] = None

        if "uid" in element.attrib:
            node["created"]["uid"] = element.attrib["uid"]
        else:
            node["created"]["uid"] = None

        if "lat" in element.attrib:
            node["pos"] = [float(element.attrib["lat"]), float(element.attrib["lon"])]

        # processing of 'tag' key-value pairs
        for tag in element.iter("tag"):
            k = tag.attrib["k"]
            v = tag.attrib["v"]

            # flag, is k-v pair processed and added to data ?
            proc = False 

            if problemchars.search(k):
                continue

            # lower case, no colon
            l = lower.search(k)
            # lower case, one colon
            l1 = lower_1_colon.search(k)
            # lower case, two colons
            l2 = lower_2_colon.search(k)
            # mixed case or digits or dash, no colon
            m = mixed.search(k)
            # mixed case or digits or dash, one colon
            m1 = mixed_1_colon.search(k)

            # lower
            if l:
                # key consists of one word only, no colon
                if k == 'wikipedia':
                    if k not in node:
                        node[k] = {}

                    # handle this case
                    # <tag k="wikipedia" v="uk:Астрономічна обсерваторія Київського університету"/>"
                    vspl = v.split(":")
                    lang = vspl[0] 
                    rest = vspl[1]
                    node[k][lang] = rest 
                    proc = True

                else:
                    # no changes
                    node[k] = v
                    proc = True

            elif l1:
                # key has one colon
                spl = k.split(":")
                p1 = spl[0]
                p2 = spl[1]

                if p1 == "abandoned":
                    node[p1] = "yes"
                    node[p2] = v

                elif p1 == "addr":
                    if p1 not in node:
                        node[p1] = {}

                    if p2 == "city" or p2 == "street":
                        if p2 not in node[p1]:
                            node[p1][p2] = {}

                        # fix of a street name according to the mapping
                        if p2 == "street":
                            v = update_name(v, mapping_uk)

                        node[p1][p2] = { "uk" : v }
                        proc = True
                    else:
                        node[p1][p2] = v
                        proc = True

                elif p1 == 'wikipedia':
                    # handle this case
                    # <tag k="wikipedia:uk" v="Парк_імені_Пушкіна_(Київ)"/>
                    if p1 not in node:
                        node[p1] = {}
                    node[p1][p2] = v 


            #mixed
            elif m:
                # key consists of one word only, no colon
                if k == "ISO3166-1":
                    if k not in node:
                        node[k] = {}
                    node[k]["alpha2"] = v 
                    proc = True

                elif k == "CEMT":
                    node["cemt"] = v
                    proc = True
            elif m1:
                # key has one colon
                spl = k.split(":")
                p1 = spl[0]
                p2 = spl[1]

                if p1 == "ISO3166-1":
                    if p1 not in node:
                        node[p1] = {}
                    node[p1][p2] = v 
                    proc = True

                elif p1 == "fuel":
                    if p1 not in node:
                        node[p1] = {}

                    if re.search(r'diesel', p2):
                        # such cases as fuel:GTL_diesel   
                        if p2 not in node[p1]:
                            node[p1]["diesel"] = {}

                        if p2 == "GTL_diesel":
                            node[p1]["diesel"] = { "GTL" : v }
                        elif p2 == "HGV_diesel":
                            node[p1]["diesel"] = { "HGV" : v }

                    elif re.search(r'octane', p2):
                        # such cases as fuel:octane_100   
                        if p2 not in node[p1]:
                            node[p1]["octane"] = {}

                        x = re.search(r'octane_(\d+)', p2)
                        node[p1]["octane"] = { x.group(1) : v }

                    else:
                        # the rest in fuel category
                        node[p1][p2] = v

                    proc = True

            elif l2:
                # key has two colons
                spl = k.split(":")
                p1 = spl[0]
                p2 = spl[1]
                p3 = spl[2]

                if p1 == "addr":
                    if p1 not in node:
                        node[p1] = {}

                    # handle keys such as addr:city:en
                    if p2 == "city" or p2 == "street":
                        if p2 not in node[p1]:
                            node[p1][p2] = {}

                        node[p1][p2] = { p3 : v }
                        proc = True

            if proc == False:
                ignored_keys[k] += 1
                #print "This key-value pair is ignored: {0} : {1}\n".format(k, v)


        for nd in element.iter("nd"):
            if "node_refs" not in node:
                node["node_refs"] = []
            node["node_refs"].append(nd.attrib["ref"])

            
            
        return node
    else:
        return None


def process_map(file_in, db):
    #file_out = "{0}.json".format(file_in)
    #data = []
    #with codecs.open(file_out, encoding = 'utf-8', mode = "w") as fo:
        #fo.write("[")
    for _, element in ET.iterparse(file_in):
        el = shape_element(element)
        if el:
            db.kyiv_map.insert(el)
                #data.append(el)
                #if pretty:
                #    fo.write(json.dumps(el, encoding="utf-8",
                #        ensure_ascii=False, indent=2)+"\n")
                #else:
                #    fo.write(json.dumps(el, encoding="utf-8", ensure_ascii=False) + "\n")
                #fo.write(",")
        #fo.write("]")
    #return data

def test():
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples

    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    process_map('../data/kyiv_ukraine.osm', db)
    print db.kyiv_map.find_one()

    ignored_keys_ordered = OrderedDict(sorted(ignored_keys.items()))
    with open("ignored_keys", "w") as f:
        for key, val in ignored_keys_ordered.iteritems():
            f.write(key + '   ' + str(val)  + '\n')
    
if __name__ == "__main__":
    start_time = time.time()
    test()
    end_time = time.time()
    print("Elapsed time: {0} s".format(end_time - start_time))
