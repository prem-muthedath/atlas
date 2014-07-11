#!/usr/bin/python

from . import tests

from . import clean

def main():
	tests.run.run_all()

if __name__=='__main__':
	main()
	clean.run()
