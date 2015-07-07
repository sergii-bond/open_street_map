#!/usr/bin/env python
"""
Runs queries
"""

import pprint

def get_db(db_name):
    from pymongo import MongoClient
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

    
#$push is similar to $addToSet. The difference is that rather than accumulating only unique values 
#it aggregates all values into an array.
