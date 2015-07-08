#!/usr/bin/env python
"""
Runs queries
"""

import pprint
import pymongo
from pymongo import MongoClient

def get_db(db_name):
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def print_result(result):
    # print the aggregation result
    for line in result:
        pprint.pprint(line)

def aggregate(db, pipeline):
    result = db.kyiv_map.aggregate(pipeline)
    return result

if __name__ == '__main__':
    db = get_db('examples')

    # Counts the number of unique users.
    pipeline = [{"$group" : {"_id" : "$created.user"}},
                {"$group" : {"_id" : "null",
                             "count" : {"$sum" : 1 }}},
                {"$limit" : 1}]
    result = aggregate(db, pipeline)
    print "Unique number of users:"
    print_result(result)

    # Counts the number of nodes
    print "Number of nodes:"
    pipeline = [{"$match" : {"type" : "node"}},
                {"$group" : {"_id" : "null",
                             "count" : {"$sum" : 1 }}},
                {"$limit" : 1}]
    result = aggregate(db, pipeline)
    print_result(result)

    # Counts the number of ways
    print "Number of ways:"
    pipeline = [{"$match" : {"type" : "way"}},
                {"$group" : {"_id" : "null",
                             "count" : {"$sum" : 1 }}},
                {"$limit" : 1}]
    result = aggregate(db, pipeline)
    print_result(result)

    # Find what's near location where I lived
    #print "What's near the place I lived:"
    #db.kyiv_map.ensure_index([("pos", pymongo.GEO2D)])
    #result = db.kyiv_map.aggregate([{ 
    #            "$geoNear" : {
    #                #"near" : { "type" : "Point", "coordinates" : [50.46117, 30.482912]},
    #                "near" : { "coordinates" : [50.46117, 30.482912]},
    #                "distanceField" : "distance.calculated",
    #                "maxDistance" : 1000,
    #                #"query" : {"type" : "node"},
    #                "limit" : 5
    #            }      
    #           }]
    #result = db.kyiv_map.find({ 
    #        "pos" : { 
    #            "$near" : {
    #                "$geometry" : {
    #                    "type" : "Point",
    #                    "coordinates" : [50.46117, 30.482912]
    #                    },
    #                "$maxDistance" : 1000,
    #            }
    #        }
    #})
    #result = db.kyiv_map.find({ 
    #        "pos" : { 
    #            "$near" : [50.46117, 30.482912]
    #  #          "$maxDistance" : 1000
    #            },
    #        "amenity" : "bank" 
    #        })
    #result = db.kyiv_map.find({ "pos" : { "$near" : [50.46117, 30.482912] }
    #    }).count()
    #print_result(result)

    # Return the list of amenities
    print "List of available amenities: "
    pipeline = [{"$match" : {"amenity" : {"$exists" : 1}}},
                {"$group" : {"_id" : "$amenity"}},
                {"$sort" : {"_id" : 1}},
                ]
    result = aggregate(db, pipeline)
    l = []
    for item in result:
        l.append(item["_id"])
    print l

    # Counts the number of unique banks
    print "Number of unique banks:"
    pipeline = [{"$match" : {"amenity" : "bank"}},
                {"$group" : {"_id" : "$name"}},
                {"$group" : {"_id" : "null",
                             "count" : {"$sum" : 1 }}},
                ]
    result = aggregate(db, pipeline)
    print_result(result)

    
#$push is similar to $addToSet. The difference is that rather than accumulating only unique values 
#it aggregates all values into an array.
