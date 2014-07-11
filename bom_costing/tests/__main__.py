#!/usr/bin/python

from .. import clean_pyc

from . import run

def main():
	run.run_all()

if __name__=='__main__':
	main()
	clean_pyc.run()
