#!/usr/bin/python

from formats.text import BomView
from formats.text import BomPartView

from formats.text import LevelTextView
from formats.text import PartTextView

class TextViewConfiguration:
	def configure(self):
		return BomView(BomPartView(LevelTextView(), PartTextView()))