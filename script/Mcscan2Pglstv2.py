#!/usr/bin/env python
import sys,re

IN1=open(sys.argv[1],'r')#xyz.coll
IN2=open(sys.argv[2],'r')#xyz.tandem

OUT1=open(sys.argv[3],'w')

OUT2=open(sys.argv[4],'w')


dict1=set()
dict2=set()
for eachline in IN1:
	if not eachline.startswith("#"):
		split=eachline.strip().split()
		if split[2].startswith("Chr"):
			dict1.add(split[2])
		if split[3].startswith("Chr"):
			dict1.add(split[3])
for eachline in IN2:
	split=eachline.rstrip().split(",")
	for g in split:
		if g.startswith("Chr"):
			dict2.add(g)


for i in dict1:
	OUT1.write("%s\n"%(i))
for i in dict2:
	OUT2.write("%s\n"%(i))

IN1.close()
IN2.close()
OUT1.close()
OUT2.close()
	
