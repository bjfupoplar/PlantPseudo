#!/usr/bin/env python
import sys,re

#scaffold_589    20315   21337   +       Potri.T153700_intron1

IN1=open(sys.argv[1],'r')#Ptrichocarpa.gene.pos
IN2=open(sys.argv[2],'r')#pseudogene.phase2
IN3=open(sys.argv[3],'r')#Ptri.pri.pep

OUT=open(sys.argv[4],'w')


dict2={}
ldict={}

#gene.pos
for eachline in IN1:
	split=eachline.rstrip().split("\t")
	dict2[split[-1]]="\t".join(split[:-1])	

#get the length of protein
for eachline in IN3:
	eachline=eachline.rstrip()
	m=re.match(">(\S+)",eachline)
	if m:
		gene=m.group(1)
		ldict[gene]=0
	else:
		ldict[gene]+=len(eachline)
	
	
#ChrM    48113   48532   +       ATMG00170

fr=IN2.readline().rstrip()
OUT.write("%s\t%s\t%s\t%s\t%s\t%s\n"%(fr,"pChr","pStart","pEnd","pStrand","Frac"))
for eachline in IN2:
	eachline=eachline.rstrip()
	split=eachline.rstrip().split("\t")
	rate=float(split[-2])/ldict[split[-1]]
	OUT.write("%s\t%s\t%s\n"%(eachline,dict2[split[-1]],rate))	

IN1.close()
IN2.close()
IN3.close()
OUT.close()
