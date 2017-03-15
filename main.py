#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Interpreter
from argparse import *
import re

if __name__ == "__main__":
	parser = ArgumentParser(description = "A Python interpreter for fλak.  A functional Brain-Flak derivative.",prog="Fλak")
	parser.add_argument(
		"source",
		metavar = "Source",
		help = "The name of the file from which the source is read."
	)
	parser.add_argument(
		"input",
		metavar = "Input",
		type = int,
		nargs = '*',
		help = 'The default method for providing input.  It will be placed on the active stack before the program begins.'
	)
	parser.add_argument(
		"--version",
		action = "version",
		version = "%(prog)s 0.0",
		help = "Prints the version number of the interpreter."
	)
	args = parser.parse_args()
	with open(args.source) as file:
		interpreter = Interpreter.Interpreter(re.sub("[^(){}<>\[\]]","",file.read()))
	interpreter.insert(args.input)
	interpreter.run()
	print "\n".join(map(str,interpreter.stacks[0][::-1]))
