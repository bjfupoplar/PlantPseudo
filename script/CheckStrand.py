#!/usr/bin/env python
import sys,re


IN1=open(sys.argv[1],'r')#ptr.q_G50.PE_I50.PS1.pairs.sw.raw
IN2=open(sys.argv[2],'r')#ptr.q_G50.PE_I50.PS1.subj_coord
OUT=open(sys.argv[3],'w')

lines=IN1.readlines()

index=0
dict={}
while(index<len(lines)):
	eachline=lines[index]
	if eachline.startswith("The best"):
		index+=1
		split=lines[index].rstrip().split()
		if split[3][1]=="f":
			strand="+"
		else:
			strand="-"
		dict[split[0]]=strand
	index+=1

num=0
for eachline in IN2:
	eachline=eachline.rstrip()
	split=eachline.split()
	name=split[0]+"|"+split[1]+"-"+split[2]
	if name in dict:
		num+=1
		OUT.write("%s\t%s\tpg_%s\n"%(eachline,dict[name],str(num)))	
	else:
		print eachline
IN1.close()
IN2.close()
OUT.close()
