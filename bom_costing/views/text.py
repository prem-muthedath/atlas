#!/usr/bin/python

class TextViewFactory:
	def view(self):
		return TextView(TextViewRow(TextViewLevel(), TextViewPart()))
		

class View(object):
	def _export(self, items):
		for each in items:
			each.export(self)

	def render(self):
		pass


class TextView(View):
	def __init__(self, view_row):
		self.__current_row=view_row
		self.__view_rows=[]

	def export_bom(self, bom_components):
		self.__current_row.export_bom(bom_components, self)

	def export_part(self, part_data):
		self.__current_row.export_part(part_data, self)

	def add_row(self, row):
		self.__view_rows.append(row)

	def render(self): 
		return self.__header()+self.__render()	

	def __header(self):
		return self.__current_row.header()

	def __render(self):
		return ''.join(self.__view_rows)


class TextViewRow():
	def __init__(self, view_level, view_part):
		self.__view_level=view_level
		self.__view_part=view_part

	def export_bom(self, bom_components, bom_view):
		self.__view_level.export_bom(bom_components, bom_view)

	def export_part(self, part_data, bom_view):
		self.__view_part._export(part_data)
		bom_view.add_row(self.render())

	def render(self): 
		return self.__format(
			self.__view_level.render(),
			self.__view_part.render())

	def header(self):
		return self.__format(
			self.__view_level.header(),
			self.__view_part.header())

	def __format(self, level_text, part_text):
		return level_text+part_text+'\n'


class TextViewLevel:
	__COLUMN_WIDTH=13
	__HEADER='Level'

	def __init__(self, value=-1):
		self.__value=value		

	def export_bom(self, bom_components, view):
		self.__enter_bom()
		view._export(bom_components)
		self.__exit_bom()

	def __enter_bom(self):
		self.__value+=1

	def __exit_bom(self):
		self.__value-=1

	def render(self):
		return self.__format().ljust(self.__COLUMN_WIDTH)

	def __format(self):
		indent=abs(self.__value)*"  "
		return indent+str(self.__value)

	def header(self):
		return self.__HEADER.center(self.__COLUMN_WIDTH)


class TextViewPart(View):
	def __init__(self):
		self.__data={'name':'', 'code':'', 'quantity':'', 'cost':''} 

	def add_name(self, name):
		self.__data["name"]=name

	def add_code(self, code):
		self.__data["code"]=code

	def add_quantity(self, quantity):
		self.__data["quantity"]=quantity

	def add_cost(self, cost):
		self.__data["cost"]=cost

	def render(self): 
		return self.__data["name"].center(65)+ \
			self.__data["code"].center(10)+ \
			self.__data["quantity"].center(10)+ \
			self.__data["cost"].center(10)

	def header(self):
		return self.__header_part().render()

	def __header_part(self):
		view_part=self.__class__()
		view_part.add_name('Part')
		view_part.add_code('Code')
		view_part.add_quantity('Quantity')
		view_part.add_cost('Cost')
		return view_part				
