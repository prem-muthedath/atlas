#!/usr/bin/python

import os

def run():
	for dirpath, subdirnames, filenames in os.walk(os.getcwd()):
		pyc_files=[os.path.join(dirpath, filename) for filename in filenames if filename.endswith(".pyc")]
		for each in pyc_files:
			os.remove(each)