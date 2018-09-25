#!/usr/bin/env python
import sys,re

IN1=open(sys.argv[1],'r')#wgd.lst

IN2=open(sys.argv[2],'r')#tandemlst

IN3=open(sys.argv[3],'r')#Pg.add.xls


IN4=open(sys.argv[4],'r')#helitron.pg.lst


OUT=open(sys.argv[5],'w')#

lst1=[]
lst2=[]
lst3=[]

for eachline in IN1:
	lst1.append(eachline.rstrip())

for eachline in IN2:
	lst2.append(eachline.rstrip())

for eachline in IN3:
	lst3.append(eachline.rstrip())


fr=IN4.readline().rstrip()

OUT.write("%s\t%s\n"%(fr,"DupType"))

tp=""
for eachline in IN4:
	split=eachline.rstrip().split("\t")
	if split[0] in lst1:
		tp="WGDDUP"
	elif split[0] in lst2:
		tp="TandemDUP"
	elif split[0] in lst3:
		tp="Helitron"
	else:
		tp="---"
	OUT.write("%s\t%s\n"%("\t".join(split),tp))
IN1.close()
IN2.close()
OUT.close()

	
