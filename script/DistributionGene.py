#!/usr/bin/env python
import sys,re

#
IN1=open(sys.argv[1],'r')#PgClss.final.out
IN2=open(sys.argv[2],'r')#
OUT=open("distribution.at.txt",'w')

wgd=[]
dup=[]
pssd=[]
frag=[]

fr=IN1.readline()
for eachline in IN1:
	split=eachline.rstrip().split("\t")
	if split[-2]=="WGDDUP":
		wgd.append(split[0])	
	elif split[-2]=="DUP":
		dup.append(split[0])
	elif split[-2]=="PSSD":
		pssd.append(split[0])
	elif split[-2]=="FRAG":
		frag.append(split[0])

print len(dup)

wgdr=[]
dupr=[]
pssdr=[]
fragr=[]

##Potri.003G014100 Chr19|33564-33681
#>236 236 75.4 9.5e-19 236 97.436 97.436 1-39:2-118

index=0
lines=IN2.readlines()

while (index<len(lines)):
	line=lines[index]
	if line.startswith("#"):
		split=line.split()
		if split[1] in wgd:
			index+=1
			line=lines[index]
			s=line.split()[-1].split("-")[0]
			wgdr.append(s)
		elif split[1] in dup: 
			index+=1
			line=lines[index]
			s=line.split()[-1].split("-")[0]
			dupr.append(s)
		elif split[1] in pssd: 
			index+=1
			line=lines[index]
			s=line.split()[-1].split("-")[0]
			pssdr.append(s)
		elif split[1] in frag: 
			index+=1
			line=lines[index]
			s=line.split()[-1].split("-")[0]
			fragr.append(s)
	index+=1


OUT.write("species"+"\t"+"distance"+"\n")

for i in wgdr:
	OUT.write("%s\t%s\n"%("WGD",i))
for j in dupr:
	OUT.write("%s\t%s\n"%("DUP",j))

for j in pssdr:
	OUT.write("%s\t%s\n"%("PSSD",j))

for j in fragr:
	OUT.write("%s\t%s\n"%("FRAG",j))


