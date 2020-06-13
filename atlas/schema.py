#!/usr/bin/python

from aenum import Enum, NoAlias

# this module defines the part schema.
################################################################################

class _Schema(Enum):
    # class design idea from /u/ ethan furman @ https://tinyurl.com/ycacxytx

    # schema definition (see below) -- members (i.e., columns) & their order.
    # "no-alias" settings from /u/ ethan furman @ https://tinyurl.com/yb2ofxvd
    _order_ = 'level part_number source_code unit_cost quantity costed cost'
    _settings_ = NoAlias

    level=int
    part_number=str
    source_code=str
    unit_cost=int
    quantity=int
    costed=str
    cost=int

    def __init__(self, _type):
        # `_type`: data type defined for the member in schema.
        self._type=_type

