
Problems encountered in the map
-------------------------------------

Audit of tags
===================

First we examine the existing tags and their quantity. For this purpose, *mapparser.py* code was written. Its output is below.

.. code-block:: python

    {'bounds': 1,
    'member': 66249,
    'nd': 1349977,
    'node': 1101522,
    'osm': 1,
    'relation': 5432,
    'tag': 448567,
    'way': 161984}


From this output we see that no unusual nodes are present. There is more than 1 million nodes in the map. However fewer than a half is tagged. 
There are around 5000 relations, but In this project we ignore them.

Audit of keys in tags
=========================

Next we want to evaluate the keys of all *tag* elements inside *node* or *way*. 
In the beginning we just take a look at all tag's keys to get a feeling of what to expect further. 
In order to implement this, the dictionary is used, where the key is a *tag key* and a value is the number of its occurences. 
The dictionary is output to a text file for visual inspection. Here is an example of a resulting file contents:

.. code-block:: console

    CEMT   32
    ISO3166-1   2
    ISO3166-1:alpha2   2
    ISO3166-1:alpha3   2
    ISO3166-1:numeric   2
    ISO3166-2   3
    _description_   275
    abandoned   38
    abandoned:amenity   12
    abandoned:building   2
    abandoned:highway   2
    ...

Seeing the list of keys we have, the good idea would be to categorize the keys by patterns.
Here is a list of regexes so far constructed that we can run our keys through:

.. code-block:: python

    #Keys that contain letters or undersore only
    lower = re.compile(r'^([a-z]|_)*$')
    #Keys that consist of two words separated by one semicolon
    lower_1_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
    #Keys that consist of three words separated by two semicolons
    lower_2_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*:([a-z]|_)*$')
    #Keys that have at least one character that may designate there is a problem with this key
    problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

If a key doesn't match anything from the list above, it is marked as *other*.
We run *tags.py* and get this output:

.. code-block:: python

    {'lower': 336401,
     'lower_1_colon': 111698,
     'lower_2_colon': 197,
     'other': 271,
     'problemchars': 0}

Luckily there are no keys with problems. However There are 271 other keys we didn't expect. 58 of them are unique. We can take a look at them (*tags.py* outputs them to a file *other_keys*).

.. code-block:: python

    CEMT   17
    ISO3166-1   1
    ISO3166-1:alpha2   1
    ISO3166-1:alpha3   1
    ISO3166-1:numeric   1
    ISO3166-2   2
    addr:interpolation_1   2
    addr:street_1   2
    amenity_1   1
    amenity_2   1
    associatedStreet   1
    cinema:3D   1
    compartment:NW   1
    currency:EUR   2
    currency:RUB   2
    currency:UAH   3
    currency:USD   2
    destination:lang:en:backward   1
    destination:lang:en:lanes   1
    ...


To process such keys, we add additional regexes:

.. code-block:: python

    mixed = re.compile(r'^([a-z]|[A-z]|_|[0-9]|-)*$')
    mixed_1_colon = re.compile(r'^([a-z]|[A-z]|_|[0-9]|-)*:([a-z]|[A-z]|_|[0-9]|-)*$')
    lower_3_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*:([a-z]|_)*:([a-z]|_)*$')


If we want to know more hints about the particular key, in this case we can use *grep* utility to learn about its value and its neighborhood.
For example, to find out more information about 'CEMT' key, this command can be run:

.. code-block:: console

    grep 'CEMT' -A 2 -B 2 kyiv_ukraine.osm

One of the outputs is:

.. code-block:: console

    <nd ref="267301603"/>
    <nd ref="1381708683"/>
    <tag k="CEMT" v="Vb"/>
    <tag k="boat" v="yes"/>
    <tag k="name" v="Дніпро"/>

There is a hint here, "Дніпро" is a river. According to Wikipedia, CEMT can stand for `Classification of European Inland Waterways <https://en.wikipedia.org/wiki/Classification_of_European_Inland_Waterways>`_. The value of *CEMT* key is *Vb*. From the same page in Wikipedia we see that it designates a type of classification of waterways. As a result, we can consider this key-value part to be valid. At this point no actions on this pair is to be taken, except we can convert CEMT to lower case. Then we can add it to the final database.

Similarly we can investigate other fields and see whether any kind of transformation is needed.

Transformations of the schema
=============================

Here is a list of suggested transformations:

* CEMT
    Convert to *cemt*

* ISO3166-1

    The file output by *tags.py* contains:

    .. code-block:: html

        ISO3166-1   1
        ISO3166-1:alpha2   1
        ISO3166-1:alpha3   1
        ISO3166-1:numeric   1


    According to the `Wikipedia page <https://en.wikipedia.org/wiki/ISO_3166-1>`_, ISO3166-1 is a standard that governs the country codes for their names.
    *alpha2* is a two-letter code, *alpha3* is a three-letter code and *numeric* is self-explanatory.
    Here is a snippet from our XML document:

    .. code-block:: html

        <tag k="ISO3166-1:alpha2" v="UA"/>  
        <tag k="ISO3166-1:alpha3" v="UKR"/> 
        <tag k="ISO3166-1:numeric" v="804"/>

    This can be transformed to such schema:

    .. code-block:: python

        ISO3166-1 : { alpha2 : "UA", 
                    alpha3 : "UKR",
                    numeric : 804 }

    We can also see one entry without a semicolon:

    .. code-block:: html

        <tag k="ISO3166-1" v="UA"/>

    In this case we assume the default is *alpha2*.

* abandoned

    The file output by *tags.py* contains: ::
   
        abandoned   19
        abandoned:amenity   6
        abandoned:building   1
        abandoned:highway   1
        abandoned:landuse   1
        abandoned:man_made   2
        abandoned:power   1
        abandoned:public_transport   3
        abandoned:railway   3

    One example is:

    .. code-block:: html

        <tag k="abandoned:railway" v="platform"/>              
        <tag k="abandoned:public_transport" v="platform"/>         
                                                                 

    We translate it to the following schema:

    .. code-block:: python

        abandoned : "yes" 
        railway : "platform" 
        public_transport : "platform"

* addr

    The file output by *tags.py* contains: ::

        addr:city   9094
        addr:city:en   7
        addr:country   99
        addr:district   1
        addr:flats   989
        addr:floor   8
        addr:housename   4
        addr:housenumber   31559
        addr:interpolation   61
        addr:interpolation_1   2
        addr:office   2
        addr:officenumber   1
        addr:place   2
        addr:postcode   2155
        addr:region   3
        addr:street   14713
        addr:street:en   9
        addr:street_1   2
        addr:suburb   327
        addr:unit   1

    The keys will be transformed into a schema using this logic: |br|
        Let's name key as K and value as V. |br|
        The first level key in the output is "address", its value is a dictionary of key-value pairs, where the keys are defined as: |br|
        If K has two semicolons:
            Split K string by semicolon into two parts. Let the second part be X.

            If X is "city" or "street":
                use { X : {"uk" : V } }
            else:
                use { X : V }

        else:
            Split K string by semicolon into three parts. Let the second part be X and third part be Y. |br|
            use { X : {Y : V} }
                    

    Example:

    .. code-block:: html

        <tag k="addr:city" v="Київ"/>
        <tag k="addr:street" v="Саксаганського вулиця"/>
        <tag k="addr:city:en" v="Kiev"/>
        <tag k="addr:postcode" v="01033"/>
        <tag k="addr:street:en" v="Saksahanskoho"/>

    Would be translated to:

    .. code-block:: python

        "address" : { "city" : { "ua" : "Київ" 
                                 "en" : "Kiev" },
                      "street" : { "en" : "Saksahanskoho",
                                   "uk" : "Саксаганського вулиця" }
                      "postcode" : 01033,
                    } 

* fuel

    Existing keys:

    .. code-block:: python

        fuel:GTL_diesel   2
        fuel:HGV_diesel   4
        fuel:biodiesel   4
        fuel:biogas   5
        fuel:cng   6
        fuel:diesel   61
        fuel:e10   2
        fuel:e85   2
        fuel:electricity   5
        fuel:lpg   52
        fuel:octane_100   11
        fuel:octane_80   1
        fuel:octane_91   12
        fuel:octane_92   33
        fuel:octane_95   73
        fuel:octane_98   30

    Example:

    .. code-block:: html

        <tag k="fuel:biodiesel" v="no"/>
        <tag k="fuel:octane_91" v="yes"/>
        <tag k="fuel:octane_95" v="yes"/>
        <tag k="fuel:octane_98" v="no"/>
        <tag k="fuel:GTL_diesel" v="no"/>
        <tag k="fuel:HGV_diesel" v="no"/>
        <tag k="fuel:octane_100" v="yes"/>
        <tag k="fuel:electricity" v="no"/>

    Apparently it describes the availability of different types of fuel, probably at the gas station. This is European system, therefore we do not see 87, 89 here.
    Instead, types 91, 95, 98, 100 are used.

    We can transform this to the following:

    .. code-block:: python
        
        fuel : { biodiesel : "yes",
                 octane : { 91 : "yes",
                            95 : "yes",
                            98 : "no",
                            100 : "yes"},
                 diesel : { GTL : "no",
                            HGV : "no"},
                 electricity : "no" }


* wikipedia

    The file output by *tags.py* contains:

    .. code-block:: html

        wikipedia   705
        wikipedia:en   11
        wikipedia:ru   197
        wikipedia:uk   47

    We can see two kinds of entries:

    .. code-block:: html

        <tag k="wikipedia:uk" v="Парк_імені_Пушкіна_(Київ)"/>
        <tag k="wikipedia" v="uk:Астрономічна обсерваторія Київського університету"/>

    Here we can use the following logic: 
        The first level key is wikipedia. Its value is a dictionary of the following key-value pairs: |br|
        If a key k has one semicolon and word before it is *wikipedia*, use the second word as a key, take v as a value; |br|
        else, we assume a value v contains a semicolon and use a word before semicolon as a key, and the words after a semicolon as a value. 


Audit and fixing of values
===========================

We choose to audit *addr:street* and *addr:street:en* values, that correspond to a native Ukrainian street name and to its English translation.
The last word in a value is expected to be one of the following, depending on the language:

.. code-block:: python

    expected_en = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place",
    "Square", "Lane", "Road", "Trail", "Parkway", "Commons"]

    expected_uk = [u"шосе", u"шлях", u"узвіз", u"тупик", u"проїзд",
    u"проспект", u"провулок", u"площа", u"набережна", u"дорога", u"вулиця", u"бульвар", u"алея"]

.. note::

    In order to let Python know we use Unicode in string literals, we need to
    insert this in the top of the source code:

    .. code-block:: python

        # -*- coding: utf-8 -*-

    Also, when using regular expressions, re.UNICODE flag must be used:

    .. code-block:: python

        street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE | re.UNICODE)

File *audit.py* prints the values which do not fullfill expectations:

.. code-block:: python

    {8: set([Срибнокильская, 8]),
    'Dragomanova': set(['Dragomanova']),
    'Revutskogo': set(['Revutskogo']),
    'Saksahanskoho': set(['Saksahanskoho']),
    'str.': set(['Sortuvalna str.']),
    Бучми: set([Бучми]),
    Васильковская: set([Большая Васильковская]),
    Декабристів: set([Декабристів]),
    Леніна: set([Леніна]),
    Лучистая: set([Лучистая]),
    Малышко: set([вул. Андрея Малышко]),
    Микільсько-Слобідська: set([вул. Микільсько-Слобідська]),
    Набережная: set([Набережная]),
    Олійника: set([Олійника]),
    Орача: set([Червоного Орача]),
    Осенняя: set([Осенняя]),
    Перемоги: set([проспект Перемоги]),
    Петлюри: set([С. Петлюри]),
    Сагайдачного: set([вул. Сагайдачного]),
    Сковороди: set([вул. Григорія Сковороди]),
    Сталинграда: set([проспект Героев Сталинграда]),
    Чернобыльская: set([Чернобыльская]),
    Чехова: set([Чехова]),
    Электротехническая: set([Электротехническая]),
    набережная: set([Днепровская набережная]),
    народів: set([Площа Дружби народів]),
    улица: set([Автодорожная улица, Приречная улица])}

There are several things we can see from this list:

* Some streets do not have type

* One street includes a house number instead of a type

* One street is in English, while belongs to a field *addr:street*, not *addr:street:en* (it was later found by *grep*)

* One of the street has type *улица*, which is a Russian word, not Ukrainian (it would be *вулиця*)

* Several street names have type *вул.*, which is an abbreviation of *вулиця*, and it is found in the beginning of a string, not in the end as expected

In the code we will handle the last case and replace  *вул.* by *вулиця* and put it at the end of the string.
To do this, we create a mapping and a function:

.. code-block:: python

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

As the result, the fixed street names are:

.. code-block:: python

    вул. Микільсько-Слобідська =>  Микільсько-Слобідська вулиця
    вул. Сагайдачного =>  Сагайдачного вулиця
    вул. Григорія Сковороди =>  Григорія Сковороди вулиця

Inserting into MongoDB
==============================

The following code snippet from *data.py* inserts a node into MongoDB right after its processing:

.. code-block:: python

    for _, element in ET.iterparse(file_in):
        el = shape_element(element)
        if el:
            db.kyiv_map.insert(el)
