#!/usr/bin/env python
import sys,re

IN1=open(sys.argv[1],'r')#wgd.lst

IN2=open(sys.argv[2],'r')#tandemlst

IN3=open(sys.argv[3],'r')#Pg.add.xls

OUT=open(sys.argv[4],'w')

lst1=[]
lst2=[]
for eachline in IN1:
	lst1.append(eachline.rstrip())

for eachline in IN2:
	lst2.append(eachline.rstrip())


fr=IN3.readline().rstrip()
OUT.write("%s\t%s\n"%(fr,"DupType"))

tp=""
for eachline in IN3:
	split=eachline.rstrip().split("\t")
	if split[0] in lst1:
		tp="WGDDUP"
	elif split[0] in lst2:
		tp="TandemDUP"
	else:
		tp="---"
	OUT.write("%s\t%s\n"%("\t".join(split),tp))
IN1.close()
IN2.close()
OUT.close()

	
