#!/usr/bin/env python
import sys,re

#scaffold_589    20315   21337   +       Potri.T153700_intron1

IN1=open(sys.argv[1],'r')#pseudogene.phase2
IN2=open(sys.argv[2],'r')#Ptrichocarpa.gene.pos

OUT=open("pseudogene.phase3",'w')

dict={}
for eachline in IN1:
	split=eachline.rstrip().split("\t")
	gene=split[4].split("_")[0]
	dict[gene]=dict.get(gene,0)+1

dict2={}
ldict={}

for eachline in IN3:
	split=eachline.rstrip().split("\t")
	split[-1]=split[-1]
	dict2[split[-1]]="\t".join(split[:-1])	
	ldict[split[-1]]=int(split[2])-int(split[1])


fr=IN2.readline().rstrip()
OUT.write("%s\t%s\t%s\t%s\t%s\t%s\n"%(fr,"pChr","pStart","pEnd","pStrand","Frac"))
for eachline in IN2:
	eachline=eachline.rstrip()
	split=eachline.rstrip().split("\t")
	rate=float(int(split[3])-int(split[2]))/ldict[split[-1]]
	OUT.write("%s\t%s\t%s\n"%(eachline,dict2[split[-1]],rate))	

IN1.close()
IN2.close()
IN3.close()
OUT.close()

	
	

