#!/usr/bin/env python
import sys,re

print ''' bed position'''

#Chr01   109341  111897  +       Potri.001G001500 pt.gene.pos

def dis(dpg,dg,chr,start,end):
	d1=[]
	d2=[]
	c1=[]
	c2=[]
	for i in dpg:
		pos=i.split("\t")
		if pos[0]==chr:
			d1.append(abs(int(start)-int(pos[1]))) # the distance between pg tss and lncRNA tss
			c1.append(pos)
	for i in dg:
		pos=i.split("\t")
		if pos[0]==chr:
			d2.append(abs(int(start)-int(pos[1]))) #the distance between gene tss and lncRNA tss
			c2.append(pos)
	if min(d1)<min(d2): #smaller  distance were selected
			return "pgdist",min(d1),chr,start,end,c1[d1.index(min(d1))]
	else:
			return "genedist",min(d2),chr,start,end,c2[d2.index(min(d2))]	
				
IN1=open(sys.argv[1],'r')#pg
IN2=open(sys.argv[2],'r')#gene
IN3=open(sys.argv[3],'r')#nonTE-lncRNA

OUT=open(sys.argv[4],'w')

dpg=[]
fr=IN1.readline()
#Chr5|17951-18085        Chr5    17951   18085   + 
for eachline in IN1:
	split=eachline.rstrip().split("\t")
	if split[4]=="+":
		start=split[2]
		end=split[3]
	else:
		start=split[3]
		end=split[2]
	pos="\t".join([split[1],start,end,split[0]])	
	dpg.append(pos)
dg=[]


#Chr01   142376  146067  +       Potri.001G002300

for eachline in IN2:
	split=eachline.rstrip().split("\t")
	if split[3]=="+":
		start=split[1]
		end=split[2]
	else:
		start=split[2]	
		end=split[1]
	pos="\t".join([split[0],start,end,split[4]])
	dg.append(pos)

OUT.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%("type","distance","lncRChr","lncRstart","lncRend","Chr","start","end"))


#Chr01   27178959        27179261        TCONS_00040684  +

fr=IN3.readline()
for eachline in IN3:
	split=eachline.rstrip().split("\t")
	if  split[4]=="+":
		start=split[1]
		end=split[2]
	else:
		start=split[2]
		end=split[1]
	chr=split[0]
	lncrna=split[3]
	try:
		(e1,e2,e3,e4,e5,e6)=dis(dpg,dg,chr,start,end)
	except:
		print "No matched chromosome"
	else:
		OUT.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(e1,e2,e3,e4,e5,lncrna,"\t".join(e6)))

IN1.close()
IN2.close()
OUT.close()
