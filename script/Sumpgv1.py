#!/usr/bin/env python
import sys,re

IN=open(sys.argv[1],'r')

OUT=open(sys.argv[2],'w')

OUT1=open("Pg.Classfication.xls",'w')

#type    distance        lncRChr lncRstart       lncRend Chr     start   end
#genedist        193     Chr1    780106  780409  Chr1    780602  781285
#genedist        815     Chr1    2816    2497    At1NC000020     Chr1    3631    5899    AT1G01010

p=0
b=0
c=0
f=0 #(head to head)
e=0
d=0
fr=IN.readline()

distant=0

OUT1.write("\t".join(["Classification","Type","distance","lncRChr","lncRstart","lncRend","lnRNA","Chromosome","Start","End","Gene/Pseudogene"])+"\n")
for eachline in IN:
	split=eachline.rstrip().split("\t")
	la=int(split[3])	
	lb=int(split[4])
	ga=int(split[7])
	gb=int(split[8])
	if int(split[1])<2000 and split[0]=="pgdist":
		if (lb<la and gb>ga):
			if ga>lb:
				p+=1
				OUT1.write("%s\t%s\n"%("Promoter associated",eachline.rstrip()))
				#print eachline
			elif lb>gb:
				f+=1
				OUT1.write("%s\t%s\n"%("Tail to Tail",eachline.rstrip()))
				#print eachline
			elif lb<gb:
				b+=1
				OUT1.write("%s\t%s\n"%("Body associated",eachline.rstrip()))
				#print eachline
		elif (la<lb and ga>gb):
			if ga<la:
				p+=1
				OUT1.write("%s\t%s\n"%("Promoter associated",eachline.rstrip()))
				#print eachline
			elif lb>gb:
				b+=1
				OUT1.write("%s\t%s\n"%("Body associated",eachline.rstrip()))
				#print eachline
			elif gb>lb:
				f+=1
				OUT1.write("%s\t%s\n"%("Tail to Tail",eachline.rstrip()))
				#print eachline
		elif (la<lb and ga<gb):
			c+=1
			OUT1.write("%s\t%s\n"%("Co-promoter associated",eachline.rstrip()))
			#print eachline
		else:
			c+=1
			OUT1.write("%s\t%s\n"%("Co-promoter associated",eachline.rstrip()))
			#print eachline
	elif int(split[1])>=2000 and split[0]=="pgdist":
		distant+=1
OUT.write("%s\t%s\n%s\t%s\n%s\t%s\n%s\t%s\n%s\t%s\n"%("promoter",p,"body",b,"Co",c,"f",f,"distant",distant))

IN.close()
OUT.close()	
