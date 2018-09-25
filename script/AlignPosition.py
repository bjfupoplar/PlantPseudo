#!/usr/bin/env python

from __future__ import division
import sys,re

IN1=open(sys.argv[1],'r')#pep.len
IN2=open(sys.argv[2],'r')#final.
IN3=open(sys.argv[3],'r')#sw.out
OUT=open(sys.argv[4],'w')

ldict={}
for eachline in IN1:
	split=eachline.rstrip().split("\t")
	ldict[split[0]]=float(split[1])

wgd=[]
dup=[]
pssd=[]
frag=[]

fr=IN2.readline()
for eachline in IN2:
        split=eachline.rstrip().split("\t")
	if float(split[7])>80:
   	     if split[-2]=="WGDDUP":
        	        wgd.append(split[0])    
	     elif split[-2]=="DUP":
       		        dup.append(split[0])
  	     elif split[-2]=="PSSD":
        	        pssd.append(split[0])
  	     elif split[-2]=="FRAG":
        	        frag.append(split[0])

#390 265 83.8 8.2e-21 265 63.636 75.325 203-278:29-252
index=0
lines=IN3.readlines()
OUT.write("%s\t%s\n"%("species","distance"))
while (index<len(lines)):
        line=lines[index]
        if line.startswith("#"):
                split=line.split()
		gene=split[0].lstrip("#")
		pg=split[1]
                index+=1
                line=lines[index]
		m=re.search("(\d+)-(\d+):",line)
		if m:
			s=int(m.group(1))
			e=int(m.group(2))
			for i in range(s,e,5):
				rate=i/float(ldict[gene])
				if pg in wgd:
					OUT.write("%s\t%s\n"%("PG",rate))
				elif pg in dup:
					OUT.write("%s\t%s\n"%("PG",rate))
				elif pg in pssd:
					OUT.write("%s\t%s\n"%("PG",rate))
				elif pg in frag:
					OUT.write("%s\t%s\n"%("PG",rate))
	index+=1

IN1.close()
IN2.close()
OUT.close()
	
	
