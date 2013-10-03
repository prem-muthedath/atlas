#!/usr/bin/python

class View:
	def __init__(self, view_part):
		self.__current_level=ViewLevel()
		self.__current_part=view_part
		self.__contents=[]		

	def export_bom(self, bom_components):
		self.__current_level.export_bom(bom_components, self)

	def export_part(self, part_data):
		self.export(part_data)
		self.__contents.append(self.__current_level.render(self.__current_part))

	def export(self, items):
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
		return ''.join(self.__contents)


class ViewLevel:
	def __init__(self, value=-1):
		self.__value=value		

	def export_bom(self, bom_components, view):
		self.__enter_bom()
		view.export(bom_components)
		self.__exit_bom()

	def __enter_bom(self):
		self.__value+=1

	def __exit_bom(self):
		self.__value-=1

	def render(self, view_part):
		return view_part.render(self.__value)


class TextViewPart:
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

	def render(self, level): 
		return self.__format_level(level)+self.__format()

	def __format_level(self, level):
		indented_level=abs(level)*"  "+str(level)
		return indented_level.ljust(13)

	def __format(self):
			return self.__data["name"].center(65)+ \
			self.__data["code"].center(10)+ \
			self.__data["quantity"].center(10)+ \
			self.__data["cost"].center(10)+'\n'

	def header(self):
		return self.__level_header()+self.__header()

	def __level_header(self):
		return 'Level'.center(13)		

	def __header(self):
		view_part=self.__class__()
		view_part.add_name('Part')
		view_part.add_code('Code')
		view_part.add_quantity('Quantity')
		view_part.add_cost('Cost')
		return view_part.__format()	