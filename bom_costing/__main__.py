#!/usr/bin/python

from . import tests

from . import clean_pyc

def main():
	tests.run.run_all()

if __name__=='__main__':
	main()
	clean_pyc.run()
