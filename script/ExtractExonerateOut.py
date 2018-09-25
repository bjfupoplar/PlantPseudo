#!/usr/bin/env python
import sys,re

IN=open(sys.argv[1],'r')
OUT=open(sys.argv[2],'w')

#Query id,Subject id,% identity,alignment length,mismatches,gap openings,q. start,q. end,s. start,s. end,e-value,bit score
#%ti\\t%qi\\t%tS\\t%qS\\t%tl\\t%ql\\t%tab\\t%tae\\t%tal\\t%qab\\t%qae\\t%qal\\t%pi\\n\
#Chr01   Potri.004G209000        +       .       50495391        790     14228391        14228704        313     289     392     103     39.81

for eachline in IN:
	if eachline.startswith("Chr"):
		split=eachline.rstrip().split("\t")
		if not split[1].startswith("exon"):
			start=int(split[7])
			end=int(split[6])
			length=abs(start-end)
			if length<5000:
				eval=(1/float(split[12]))*0.000001
				OUT.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(split[1],split[0],split[12],split[11],"2","2",split[9],split[10],split[6],split[7],eval,"200"))

IN.close()	
OUT.close()
