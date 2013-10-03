#!/usr/bin/python

class TextView:
	def __init__(self):
		self.__current_part=TextViewPart()
		self.__parts=[]		

	def export_bom(self, bom_components):
		self.__current_part.export_bom(bom_components, self)

	def export_part(self, part_data):
		self._export(part_data)
		self.__parts.append(self.__current_part.render())

	def _export(self, items):
		for each in items:
			each.export(self)

	def add_name(self, name):
		self.__current_part.add_name(name)

	def add_code(self, code):
		self.__current_part.add_code(code)

	def add_quantity(self, quantity):
		self.__current_part.add_quantity(quantity)

	def add_cost(self, cost):
		self.__current_part.add_cost(cost)

	def render(self): 
		return self.__header()+self.__format()	

	def __header(self):
		return self.__current_part.header()

	def __format(self):
		return ''.join(self.__parts)


class TextViewPart:
	def __init__(self):
		self.__level=TextViewLevel()
		self.__data={'name':'', 'code':'', 'quantity':'', 'cost':''} 

	def export_bom(self, bom_components, view):
		self.__level.export_bom(bom_components, view)

	def add_name(self, name):
		self.__data["name"]=name

	def add_code(self, code):
		self.__data["code"]=code

	def add_quantity(self, quantity):
		self.__data["quantity"]=quantity

	def add_cost(self, cost):
		self.__data["cost"]=cost

	def render(self): 
		return self.__level.render()+self.__format()

	def __format(self):
			return self.__data["name"].center(65)+ \
			self.__data["code"].center(10)+ \
			self.__data["quantity"].center(10)+ \
			self.__data["cost"].center(10)+'\n'

	def header(self):
		return self.__level.header()+self.__header_part().__format()

	def __header_part(self):
		view_part=self.__class__()
		view_part.add_name('Part')
		view_part.add_code('Code')
		view_part.add_quantity('Quantity')
		view_part.add_cost('Cost')
		return view_part	


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
