#!/usr/bin/env python
import sys,re,os

in1=open(sys.argv[1],'r')#
in2=open(sys.argv[2],'r')#
in3=open(sys.argv[3],'r')#
in4=open(sys.argv[4],'r')#


 #=============================================================
 # pgfile format: pgId pgChr pgStart pgEnd pgStrand frac expect ident fshift stop numOfIntrons intronPos Polya pId Pch pStart pEnd paln pIntron
 #============================================================= [zz]

polya={}
strand={}
parent={}
disable={}
intron={}
expect={}
pglst=[]

#Chr19   5260    5382    +       pg_1    24      367     AATAGGAGCAGAATTTCATGATATAGCAACCACAATACGAACTAGAGAAA              0

for eachline in in1:
	split=eachline.rstrip().split("\t")
	pgid=split[0]+"|"+split[1]+"-"+split[2]
	polya[pgid]=split[-1]
	strand[pgid]=split[3]
	pglst.append(pgid)

outtmp=open("tmp1.out","w")
for pgid in pglst:
	pgChr=pgid.split("|")[0]
	pgStart=pgid.split("|")[1].split("-")[0]
	pgEnd=pgid.split("|")[1].split("-")[1]
	outtmp.write("%s\t%s\t%s\t%s\t%s\t%s\n"%(pgid,pgChr,pgStart,pgEnd,strand[pgid],polya[pgid]))
outtmp.close()


Paln={}
#>493 265 83.8 8.8e-21 299 47.205 48.447 203-284:29-510


lines=in4.readlines()
index=0
while (index<len(lines)):
	if lines[index].startswith("#"):
		pgid=lines[index].split()[1]
		index+=1
		if lines[index].startswith("#"):
			pass
		else:
			split=lines[index].split()
			expect[pgid]="\t".join([split[3],split[5]])
			split2=split[-1].split(":")
			split3=split2[0].split("-")
			leng=float(split3[1])-float(split3[0])+1
			Paln[pgid]=leng
	index+=1


		
intmp=open("tmp1.out","r")
outtmp=open("tmp2.out",'w')

for eachline in intmp:
	eachline=eachline.rstrip()
	split=eachline.rstrip().split()
	if split[0] in expect:
		outtmp.write("%s\t%s\n"%(eachline,expect[split[0]]))
outtmp.close()
intmp.close()

cmd="rm -rf %s"%("tmp1.out")
os.system(cmd)

##Potri.001G198200 Chr04|3533391-3533533 122-161:134-14 1.2e-12 0 0 1 0
for eachline in in2:
	m=re.match("#",eachline)
	if m:
		split=eachline.rstrip().split()
		parent[split[1]]=split[0][1:]
		disable[split[1]]="\t".join([split[-4],split[-3],split[-2],split[-1]])
		
intmp=open("tmp2.out","r")
outtmp=open("tmp3.out",'w')
for eachline in intmp:
	eachline=eachline.rstrip()
	split=eachline.rstrip().split()
	outtmp.write("%s\t%s\n"%(eachline,disable[split[0]]))
outtmp.close()
intmp.close()

cmd="rm -rf %s"%("tmp2.out")
os.system(cmd)

##Potri.019G044900       Chr19|33234-51682       2       60-311;420-18323
for eachline in in3:
	split=eachline.rstrip("\n").split("\t")
	intron[split[1]]="\t".join([split[2],split[3]])

intmp=open("tmp3.out","r")
outtmp=open("pseudogene.phase2",'w')

outtmp.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%\
		("pgId","pgChr","pgStart","pgEnd","pgStrand","pgpolyA","expect","ident","stop1","stop2","fShift1","fShift2","numofIntrons","intronPos","paln","pId"))

for eachline in intmp:
	eachline=eachline.rstrip()
	split=eachline.rstrip().split()
	outtmp.write("%s\t%s\t%s\t%s\n"%(eachline,intron[split[0]],Paln[split[0]],parent[split[0]]))

outtmp.close()
intmp.close()
cmd="rm -rf %s"%("tmp3.out")
os.system(cmd)


#Potri.012G049800 Chr19|108099-108192
#>149 149 49.6 1.8e-11 149 80.645 96.774 80-110:94-2

in1.close()
in2.close()
in3.close()
in4.close()

	
