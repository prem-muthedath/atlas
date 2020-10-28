#!/usr/bin/python

from .schema import _Schema, Costed

from collections import OrderedDict

################################################################################

class _Report(object):
    def __init__(self, schema, contents):
        assert schema != None and _Schema._has(list(schema)), 'bad schema.'
        self.__schema=schema
        self.__contents=[] if schema==[] else [self.__line(i) for i in contents]

    def __line(self, item):
        line=[(i, item[i]) for i in self.__schema if item.has_key(i)]
        assert len(line) == len(self.__schema), 'line does not contain schema.'
        return OrderedDict(line)

    def _render(self):
        return self._empty() if self.__contents==[] else self._render_()

    def _empty(self):
        pass

    def _render_(self):
        pass

    def _capitalize(self):
        return [i._capitalize() for i in self.__schema]

    def _title(self):
        return 'Atlas Bill of Materials Report'

    def _body(self):
        return [(i+1, self.__format(j)) for i, j in enumerate(self.__contents)]

    def __format(self, line):
        items=OrderedDict()
        for (col, val) in line.items():
            items[col]='$'+ str(val) if col._is_money() else str(val)
        return items

    def _names(self):
        return [i for i in self.__schema]

    def _totals(self):
        totals=OrderedDict()
        cols=[self.__col(col) for col in self.__summables()]
        for (col, vals) in cols:
            totals[col]=self.__sum(col, vals)
        return self.__format(totals)

    def __summables(self):
        return [i for i in self.__schema if i in _Schema._summables()]

    def __col(self, col):
        return (col, [line[col] for line in self.__contents])

    def __sum(self, col, vals):
        if col == _Schema.costed:
            return sum([1 if val == Costed.YES else 0 for val in vals])
        return sum(vals)

    def _note(self):
        summables=self.__summables()
        return _Note(summables) if summables != [] else None

################################################################################

class _Note:
    def __init__(self, summables):
        self.__summables=["'" + i.name + "'" for i in summables]
        self.__note="Note: Totals computed only for"

    def __str__(self):
        return self.__note + " " + ", ".join(self.__summables) + "."

################################################################################

class _TextReport(_Report):
    def _empty(self):
        return _TextView([])._render()

    def _render_(self):
        sections=self.__header() + self.__body() + self.__footer()
        return _TextView(sections)._render()

    def __header(self):
        cols=['Item'] + self._capitalize()
        return self.__sections([(_TextTitle, self._title()), (_TextData, [cols])])

    def __sections(self, sections):
        size=len(self._names()) + 1
        return [i._new(size, j) for (i, j) in sections]

    def __body(self):
        data=[self.__row(i, row) for (i, row) in self._body()]
        return self.__sections([(_TextData, data)])

    def __row(self, index, row):
        if row.has_key(_Schema.level):
            level=row[_Schema.level]
            indent=(int(level))*"  "
            row[_Schema.level]=indent+level
        return [str(index)] + row.values()

    def __footer(self):
        totals=self._totals()
        if len(totals) == 0: return []
        return self.__sections([self.__totals(totals), self.__note()])

    def __totals(self, totals, caption=['Totals']):
        data=[totals[i] if totals.has_key(i) else '' for i in self._names()]
        return (_TextData, [caption + data])

    def __note(self):
        return (_TextNote, self._note())

################################################################################

class _TextView(object):
    def __init__(self, sections):
        self.__sections=sections

    def _render(self):
        if len(self.__sections)==0: return ''
        results=[]
        for section in self.__sections:
            results+=section._render()
        return '\n'.join(results)

################################################################################

class _TextGrid(object):
    def __init__(self, size):
        self.__size=size
        self.__field_width=20
        self.__sep='|'

    def _render(self):
        pass

    def _row(self, cells):
        assert len(cells) == self.__size
        data=self.__sep.join([self.__centered(i) for i in cells])
        return self.__sep.join(['', data, ''])

    def __centered(self, value):
        return value.center(self.__field_width)

    def _width(self):
        return self.__size*self.__field_width + self.__sep_width()

    def __sep_width(self):
        return self.__sep_count()*len(self.__sep)

    def __sep_count(self):
        return self.__size + 1


class _TextRow(_TextGrid):
    def __init__(self, cells):
        super(_TextRow, self).__init__(len(cells))
        self.__cells=cells

    def _render(self):
        return self._row(self.__cells)

################################################################################

class _TextSection(_TextGrid):
    def __init__(self, size):
        super(_TextSection, self).__init__(size)
        self.__border='-'

    def _render(self):
        pass

    def _border(self):
        return self.__border * self._width()


class _TextData(_TextSection):
    def __init__(self, size, rows):
        super(_TextData, self).__init__(size)
        self.__rows=rows

    @classmethod
    def _new(cls, size, rows):
        return _TextData(size, [_TextRow(i) for i in rows])

    def _render(self):
        return [row._render() for row in self.__rows] + [self._border()]


class _TextTitle(_TextSection):
    def __init__(self, size, caption):
        super(_TextTitle, self).__init__(size)
        self.__caption=caption

    @classmethod
    def _new(cls, size, caption):
        return _TextTitle(size, caption)

    def _render(self):
        return [self.__caption.center(self._width()), self._border()]


class _TextNote(_TextSection):
    def __init__(self, size, note):
        super(_TextNote, self).__init__(size)
        self.__note=note

    @classmethod
    def _new(cls, size, note):
        return _TextNote(size, note)

    def _render(self):
        return [self.__note.__str__().ljust(self._width())]

################################################################################

class _XmlReport(_Report):
    def __init__(self, schema, contents):
        super(_XmlReport, self).__init__(schema, contents)
        self.__row=None

    def _empty(self):
        return _Xsd(self)._handle_empty()._render()

    def _render_(self):
        return _Xsd(self)._handle()._render()

    def _xml_(self, nodes):
        result=[node._handle(self) for node in nodes]
        return _XmlNode('xml', [i for i in result if i !=None])

    def _title_(self):
        return _XmlElement('title', self._title())

    def _parts_(self, node):
        result=[]
        for (_, line) in self._body():
            self.__row=line
            result.append(node._handle(self))
        return _XmlNode('parts', result)

    def _part_(self):
        return _XmlNode('part', self.__elements())

    def _totals_(self):
        self.__row=self._totals()
        if len(self.__row) == 0: return None
        return _XmlNode('totals', self.__elements())

    def __elements(self):
        return [_XmlElement(i.name, j) for (i, j) in self.__row.items()]

    def _note_(self):
        note=self._note()
        return _XmlElement('note', note) if note != None else None

################################################################################

class _Xsd:
    def __init__(self, report):
        self.__report=report

    def _handle(self):
        return self.__handle([_XmlTitle, _XmlParts, _XmlTotals, _XmlNote])

    def _handle_empty(self):
        return self.__handle([])

    def __handle(self, nodes):
        return self.__report._xml_(nodes)


class _XmlTitle:
    @classmethod
    def _handle(cls, report):
        return report._title_()

class _XmlParts:
    @classmethod
    def _handle(cls, report):
        return report._parts_(_XmlPart)


class _XmlPart:
    @classmethod
    def _handle(cls, report):
        return report._part_()


class _XmlTotals:
    @classmethod
    def _handle(cls, report):
        return report._totals_()


class _XmlNote:
    @classmethod
    def _handle(cls, report):
        return report._note_()

################################################################################

class _Xml(object):
    def __init__(self, tag):
        self.__tag=tag

    def _render(self):
        pass

    def _element(self, value):
        return '<' + self.__tag + '>' + value + '</' + self.__tag + '>'


class _XmlNode(_Xml):
    def __init__(self, tag, children):
        super(_XmlNode, self).__init__(tag)
        self.__children=children

    def _render(self):
        sep='\n' if len(self.__children) > 0 else ''
        value=sep + sep.join([i._render() for i in self.__children]) + sep
        return self._element(value)


class _XmlElement(_Xml):
    def __init__(self, tag, value):
        super(_XmlElement, self).__init__(tag)
        self.__value=value

    def _render(self):
        return self._element(str(self.__value))

################################################################################

