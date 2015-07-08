
Overview of the Data
-------------------------------------

* Size of the file *kyiv_ukraine.osm* : 234 MB
* Number of unique users : 1392

    .. code-block:: python

        pipeline = [{"$group" : {"_id" : "$created.user"}},
                    {"$group" : {"_id" : "null",
                                "count" : {"$sum" : 1 }}},
                    {"$limit" : 1}]

        db.kyiv_map.aggregate(pipeline)


* Number of nodes : 1101493

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

* List of available amenities: 

    .. code-block:: python

        pipeline = [{"$match" : {"amenity" : {"$exists" : 1}}},
                        {"$group" : {"_id" : "$amenity"}},
                        {"$sort" : {"_id" : 1}},
                        ]
        result = aggregate(db, pipeline)
        l = []
        for item in result:
            l.append(item["_id"])
        print l

        [u'agency', u'arts_centre', u'atm', u'bank', u'bar', u'bbq', u'beauty', u'bench', u'bicycle_parking', u'bicycle_rental', 
        u'biergarten', u'boat_rental', u'bookmaker', u'bureau_de_change', u'bus_station', u'cafe', u'canteen', u'car_rental', 
        u'car_sharing', u'car_wash', u'casino', u'chemist', u'cinema', u'clinic', u'clock', u'club', u'college', u'community_center', 
        u'community_centre', u'construction', u'courthouse', u'coworking_space', u'crematorium', u'dentist', u'dispancery', u'doctors', 
        u'dormitory', u'drinking_water', u'driving_school', u'education', u'educational', u'educational_institute', u'embassy', u'emergency_phone', 
        u'emergency_service', u'exhibition_center', u'exhibition_hall', u'fast_food', u'ferry_terminal', u'fire_station', u'fitness_center', 
        u'food_court', u'fountain', u'fuel', u'government', u'grave_yard', u'grocery', u'gym', u'hospital', u'ice_rink', u'internet_access', 
        u'internet_cafe', u'kindergarten', u'kiosk', u'kitchen', u'library', u'lottery', u'marketplace', u'medical', u'monastery', u'nightclub', 
        u'nursing_home', u'office', u'parking', u'parking_entrance', u'parking_space', u'pawnbrocker', u'payment_terminal', u'pet', u'pharmacy', 
        u'place_of_worship', u'playground', u'police', u'post_box', u'post_office', u'post_office;bank;atm', u'pub', u'public_building', u'recycling', 
        u'register_office', u'rescue_station', u'restaurant', u'retirement_home', u'sanatorium', u'sauna', u'school', u'shelter', u'shop', u'ski_rental', 
        u'social_facility', u'stripclub', u'studio', u'substation', u'swimming_pool', u'taxi', u'telephone', u'theatre', u'thermometer', u'toilets', 
        u'tourism', u'townhall', u'translation', u'university', u'vehicle_inspection', u'vehicle_ramp', u'vending_machine', u'veterinary', 
        u'waste_basket', u'waste_disposal', u'wedding']


* Number of unique banks : 246

    .. code-block:: python

        pipeline = [{"$match" : {"amenity" : "bank"}},
            {"$group" : {"_id" : "$name"}},
            {"$group" : {"_id" : "null",
                            "count" : {"$sum" : 1 }}},
            ]
        db.kyiv_map.aggregate(pipeline)

