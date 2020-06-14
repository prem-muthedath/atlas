#!/usr/bin/python

from aenum import Enum, NoAlias

# this module defines the schema for the entire atlas app.
################################################################################

class _Schema(Enum):
    # defines atlas part schema.
    # the schema provides a central data map to exchange data within atlas.
    # classes use either this schema or a subset of it, but in both cases, 
    # classes may order the schema members per their needs.
    # class design idea from /u/ ethan furman @ https://tinyurl.com/ycacxytx

    # atlas part schema definition (see below) -- members & their order.
    # "no-alias" settings from /u/ ethan furman @ https://tinyurl.com/yb2ofxvd
    _order_ = 'level part_number source_code unit_cost quantity costed cost'
    _settings_ = NoAlias

    level=int           # part's level in the BOM tree
    part_number=str     # part's number or name
    source_code=str     # code identifying site where part is sourced from
    unit_cost=int       # cost for 1 part
    quantity=int        # number of parts of a given part number in the BOM
    costed=str          # flag denotes if part's cost is included in BOM's cost
    cost=int            # total cost of all parts of a given part number in BOM

    def __init__(self, _type):
        # `_type`: data type defined for the member in schema.
        self._type=_type


# part costed status in BOM
Costed=Enum('Costed', 'Y N')

