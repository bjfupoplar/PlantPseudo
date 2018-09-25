#!/usr/bin/env python
import sys,re

in1=open(sys.argv[1],'r')#overlap.out
out=open(sys.argv[2],'w')

d1=set()
pg=""
#Potri.013G024400        Chr01   26564992        26567636        -       2       Chr01|26564141-26565074;
for eachline in in1:
	split=eachline.rstrip().split("\t")
	pg=split[6].split(";")
	for i in pg:
		d1.add(i)
for j in d1:
	out.write("%s\n"%(j))

in1.close()
out.close()
