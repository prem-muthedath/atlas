#!/usr/bin/python

from formats.text import BomTextView
from formats.text import BomPartTextView
from formats.text import LevelTextView
from formats.text import PartTextView

class TextViewConfiguration:
	def configure(self):
		return BomTextView(BomPartTextView(LevelTextView(), PartTextView()))