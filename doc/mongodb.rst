
Overview of the Data
-------------------------------------

* Size of the file *kyiv_ukraine.osm* : 234 MB
* Number of unique users : 1392
    The following query was used:

    .. code-block:: python

        pipeline = [{"$group" : {"_id" : "$created.user"}},
                    {"$group" : {"_id" : "null",
                                "count" : {"$sum" : 1 }}},
                    {"$limit" : 1}]

        db.kyiv_map.aggregate(pipeline)


* Number of nodes : 1101493
    The following query was used:

    .. code-block:: python

        pipeline = [{"$match" : {"type" : "node"}},
                    {"$group" : {"_id" : "null",
                                "count" : {"$sum" : 1 }}},
                    {"$limit" : 1}]

        db.kyiv_map.aggregate(pipeline)

* Number of ways : 161846

    .. code-block:: python

        pipeline = [{"$match" : {"type" : "way"}},
                    {"$group" : {"_id" : "null",
                                "count" : {"$sum" : 1 }}},
                    {"$limit" : 1}]

        db.kyiv_map.aggregate(pipeline)
