#!/usr/bin/python

from aenum import Enum, NoAlias

# this module defines the schema for the entire atlas app.
################################################################################

class Costed(Enum):
# part costed status in BOM
    YES='Y'
    NO='N'

    def __str__(self):
        return self.value

################################################################################

class _Schema(Enum):
    # defines atlas part schema.
    # the schema provides a central map for data exchange in atlas.
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
    unit_cost=int       # cost for 1 part of a given a part number
    quantity=int        # number of parts of a given part number in the BOM
    costed=Costed       # flag denotes if part's cost is included in BOM's cost
    cost=int            # total cost of all parts of a given part number in BOM

    def __init__(self, _type):
        # `_type`: data type defined for the member in schema.
        self._type=_type

    @classmethod
    def _has(cls, items):
        try:
            return all([i in _Schema for i in items])
        except TypeError:
            return False

    def _is_money(self):
        return self in [_Schema.unit_cost, _Schema.cost]

    @classmethod
    def _summables(cls, cols):
        result=[]
        for col in cols:
            col.__add_to_summables(result)
        return result

    def __add_to_summables(self, summables):
        if self.__summable():
            summables.append(self)

    def __summable(self):
        return self in [_Schema.quantity, _Schema.costed, _Schema.cost]

    @classmethod
    def _capitalize(cls, cols):
        return [i.__capitalize() for i in cols]

    def __capitalize(self):
        return ' '.join(each[:1].upper()+each[1:].lower() \
                for each in self.name.split('_'))

################################################################################


