#!/usr/bin/python

from .schema import _Schema, Costed

from collections import OrderedDict

################################################################################

class _Report(object):
    def __init__(self, schema, contents):
        assert schema != None and _Schema._has(list(schema)), 'bad schema.'
        self.__schema=schema
        self.__contents=_Contents([self.__line(i) for i in contents])

    def __line(self, item):
        line=[(i.name, item[i]) for i in self.__schema if item.has_key(i)]
        assert len(line) == self._size(), 'line does not contain schema.'
        return OrderedDict(line)

    def _size(self):
        return len(self.__schema)

    def _render(self):
        return self.__contents._render(self)

    def _empty(self):
        pass

    def _render_(self):
        pass

    def _title(self):
        return 'Atlas Bill of Materials Report'

    def _body(self):
        return self.__contents._lines()

    def _col_headers(self):
        return [i._capitalize() for i in self.__schema]

    def _totals(self):
        return self.__contents._totals(self.__summables())

    def __summables(self):
        return [i.name for i in self.__schema if i in _Schema._summables()]

    def _names(self):
        return [i.name for i in self.__schema]

    def _note(self):
        summables=self.__summables()
        return _Note(summables) if summables != [] else None

################################################################################

class _Contents:
    def __init__(self, contents):
        self.__contents=[i for i in contents if len(i) > 0]

    def _render(self, report):
        return report._empty() if self.__contents == [] else report._render_()

    def _lines(self):
        return [(i+1, self.__format(j)) for i, j in enumerate(self.__contents)]

    def __format(self, line):
        items=OrderedDict()
        for (col, val) in line.items():
            items[col]='$'+ str(val) if col in _Schema._moneys() else str(val)
        return items

    def _totals(self, summables):
        if summables==[]: return None
        totals=OrderedDict()
        cols=[self.__col(col) for col in summables]
        for (col, vals) in cols:
            totals[col]=self.__sum(col, vals)
        return self.__format(totals)

    def __col(self, col):
        return (col, [line[col] for line in self.__contents])

    def __sum(self, col, vals):
        if col == _Schema.costed.name:
            return sum([1 if val == Costed.YES else 0 for val in vals])
        return sum(vals)

################################################################################

class _Note:
    def __init__(self, summables):
        self.__summables=["'" + i + "'" for i in summables]
        self.__note="Note: Totals computed only for"

    def __str__(self):
        return self.__note + " " + ", ".join(self.__summables) + "."

################################################################################

class _TextReport(_Report):
    def _empty(self):
        return _Tsd(self)._render_empty()

    def _render_(self):
        return _Tsd(self)._render()

    def _text_(self, nodes):
        sections=[node._handle(self) for node in nodes]
        return _TextView(sections)._render()

    def _title_(self):
        return self.__section(_TextTitleSection, self._title())

    def __section(self, section, val):
        size=self._size() + 1
        return section._new(size, val)

    def _header_(self):
        cols=['Item'] + self._col_headers()
        return self.__section(_TextDataSection, [cols])

    def _body_(self):
        data=[_TextRow(i, row)._format() for (i, row) in self._body()]
        return self.__section(_TextDataSection, data)

    def _totals_(self):
        totals=self._totals()
        if totals==None: return None
        return self.__section(_TextDataSection, self.__totals(totals))

    def __totals(self, totals):
        names=OrderedDict([(i, '') for i in self._names()])
        names.update(totals)
        return [['Totals'] + names.values()]

    def _note_(self):
        note=self._note()
        return self.__section(_TextNoteSection, note) if note != None else None

################################################################################

class _Tsd:
    def __init__(self, report):
        self.__report=report

    def _render_empty(self):
        return self.__render([])

    def _render(self):
        nodes=[self.Title, self.Header, self.Body, self.Totals, self.Note]
        return self.__render([node() for node in nodes])

    def __render(self, nodes):
        return self.__report._text_(nodes)

    class Title:
        def _handle(self, report):
            return report._title_()

    class Header:
        def _handle(self, report):
            return report._header_()

    class Body:
        def _handle(self, report):
            return report._body_()

    class Totals:
        def _handle(self, report):
            return report._totals_()

    class Note:
        def _handle(self, report):
            return report._note_()

################################################################################

class _TextRow:
    def __init__(self, index, row):
        self.__index=index
        self.__row=row
        self.__field=_Schema.level.name

    def _format(self):
        return self.__format(self.__row.items())

    def __format(self, items):
        row=[self.__level(j) if i == self.__field else j for (i, j) in items]
        return [str(self.__index)] + row

    def __level(self, level):
            indent=(int(level))*"  "
            return indent+level

################################################################################

class _TextView(object):
    def __init__(self, sections):
        self.__sections=[i for i in sections if i != None]

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


class _TextRowGrid(_TextGrid):
    def __init__(self, cells):
        super(_TextRowGrid, self).__init__(len(cells))
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


class _TextDataSection(_TextSection):
    def __init__(self, size, rows):
        super(_TextDataSection, self).__init__(size)
        self.__rows=rows

    @classmethod
    def _new(cls, size, rows):
        return _TextDataSection(size, [_TextRowGrid(i) for i in rows])

    def _render(self):
        return [row._render() for row in self.__rows] + [self._border()]


class _TextTitleSection(_TextSection):
    def __init__(self, size, caption):
        super(_TextTitleSection, self).__init__(size)
        self.__caption=caption

    @classmethod
    def _new(cls, size, caption):
        return _TextTitleSection(size, caption)

    def _render(self):
        return [self.__caption.center(self._width()), self._border()]


class _TextNoteSection(_TextSection):
    def __init__(self, size, note):
        super(_TextNoteSection, self).__init__(size)
        self.__note=note

    @classmethod
    def _new(cls, size, note):
        return _TextNoteSection(size, note)

    def _render(self):
        return [self.__note.__str__().ljust(self._width())]

################################################################################

class _XmlReport(_Report):
    def __init__(self, schema, contents):
        super(_XmlReport, self).__init__(schema, contents)
        self.__row=None

    def _empty(self):
        return _Xsd(self)._render_empty()

    def _render_(self):
        return _Xsd(self)._render()

    def _xml_(self, nodes):
        result=[node._handle(self) for node in nodes]
        return _XmlNode('xml', [i for i in result if i !=None])._render()

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
        if self.__row == None: return None
        return _XmlNode('totals', self.__elements())

    def __elements(self):
        return [_XmlElement(i, j) for (i, j) in self.__row.items()]

    def _note_(self):
        note=self._note()
        return _XmlElement('note', note) if note != None else None

################################################################################

class _Xsd:
    def __init__(self, report):
        self.__report=report

    def _render(self):
        nodes=[self.Title, self.Parts, self.Totals, self.Note]
        return self.__render([node() for node in nodes])

    def _render_empty(self):
        return self.__render([])

    def __render(self, nodes):
        return self.__report._xml_(nodes)

    class Title:
        def _handle(self, report):
            return report._title_()

    class Parts:
        def _handle(self, report):
            return report._parts_(self.Part())

        class Part:
            def _handle(self, report):
                return report._part_()

    class Totals:
        def _handle(self, report):
            return report._totals_()

    class Note:
        def _handle(self, report):
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

