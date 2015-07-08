
Other ideas about the datasets
-------------------------------------

* Find more information about fields. For instance:
    * information about *addr:interpolation* field can be found `here <http://wiki.openstreetmap.org/wiki/Addresses#Using_interpolation>`_. 
    * see how *addr:interpolation_1*  can interpreted.
    * understand what does *addr:street_1* designate.
    * *Possible issues*:
        * Not all information can be found online
        * Information found online or intuition may be different from the actual meaning by a user
        * Some fields can be input by a user mistakenly and have no relation to the node

* Resolve entities. It is likely several fields in the current solution mean the same thing, for example, *shop*, *shop_1* and *shop_2*.
    * *Possible issues*:
        * As the dataset increases, manual approach is tedious. Machine learning techniques can be applied to learns from a user feedback - expensive to implement in terms of resources and time.

* Process other unique keys that have one or more columns (:) inside, convert them to a better schema.
    * *Possible issues*:
        * Lack of consistency: for example, in one case a field is *name:uk* and in another can be *name:ukr*.

* Audit the values
    * See whether any values contain information that can be extracted as a new field (we have seen this in wikipedia's value already). Clean up if the pattern can be discovered.
    * Check consistency, for example of units. 
    * *Possible issues*:
        * Because the data includes languages other than English, there may be issues with matching using regular expressions. Before making a regex for unicode, one needs to understand well the differences compared to ascii regex.

* Process documents of type *relations* to get more data about the city into the database.
    * *Possible issues*:
        * *relation* may include a reference to a node that is not in the current dataset.

* After the better schema is in place and the understanding of the fields meaning is clear, more sophisticated queries can be run to answer many questions about the city.
    * *Possible issues*:
        * Some documents will not have a key/value pair for a quieried field. If there is no key/value, it doesn't necessarily mean it is not applicable for the document. A user may not have specified it. The results can be biased.

* Provisions should be made on updating the database periodically with new data coming from Open Street Map. If possible, find a way to do it incrementally, without a need to completely write the data from scratch.
    * *Possible issues*:
        * Implementation can be costly

