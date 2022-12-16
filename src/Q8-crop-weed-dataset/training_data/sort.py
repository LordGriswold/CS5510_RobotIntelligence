#!/usr/bin/env python
import sys, os, glob

for file in glob.glob("*.txt"):
	name = file.split('.')[0]
	print(f"{name = }")
	with open(file) as infile:
		text = infile.readlines()
		print(f"{text[0][0]}")
		if (text[0][0] == "0"):
			os.rename(f"{name}.jpeg", f"crops/{name}.jpeg")
		else:
			os.rename(f"{name}.jpeg", f"weeds/{name}.jpeg")
	

