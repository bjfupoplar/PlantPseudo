#!/usr/bin/env python
import sys,re

IN=open(sys.argv[1],'r')#pseudogene.3
OUT=open(sys.argv[2],'w')

fr=IN.readline()
OUT.write(fr)
for eachline in IN:
	split=eachline.rstrip().split("\t")
	if float(split[-1])>=0.05 and float(split[-7])>30:
		OUT.write(eachline)

IN.close()
OUT.close()
	
