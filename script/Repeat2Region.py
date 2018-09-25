#!/usr/bin/env python
import sys,re

in1=open(sys.argv[1],'r')#repeatmasked
in2=open(sys.argv[2],'r')#Pg.add.xls
out1=open(sys.argv[3],'w')
out2=open(sys.argv[4],'w')



strand=""
num=0
fr=in1.readline()
for eachline in in1:
	split=eachline.rstrip().split()
	if len(split)>2 and split[9].upper().startswith("HELITRON"):
		if split[8]=="C":
			strand="-"
		else:
			strand="+"
		num+=1
		out1.write("%s\t%s\t%s\t%s\t%s_%s\n"%(split[4],split[5],split[6],strand,split[9],num))

fr=in2.readline()
#Chr02|2960109-2960404   Chr02   2960109 2960404 -
for eachline in in2:
	split=eachline.rstrip().split("\t")
	out2.write("%s\t%s\t%s\t%s\t%s\n"%(split[1],split[2],split[3],split[4],split[0]))
	
in1.close()
out1.close()
out2.close()

