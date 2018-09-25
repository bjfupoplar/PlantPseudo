#!/usr/bin/env python
import sys,re

IN=open(sys.argv[1],'r')
OUT1=open("pg.gff",'w')
OUT2=open("pg.blast",'w')

#pgId    pgChr   pgStart pgEnd   pgStrand        pgpolyA expect  ident   stop1   stop2   fShift1 fShift2 numofIntrons    intronPos       pId
#ChrM|28733-28868        ChrM    28733   28868   -       0       3.9e-22 100.000 0       0       0       0       0       ---     ATMG00690

fr=IN.readline()
for eachline in IN:
	split=eachline.rstrip().split("\t")
	OUT1.write("sp#%s\t%s\t%s\t%s\n"%(split[1],split[0],split[2],split[3]))
	alleng=str(int(split[3])-int(split[2]))
	OUT2.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(split[15],split[0],split[7],alleng,"2","2",split[2],split[3],split[16],split[17],split[6],"200"))
	
IN.close()
OUT1.close()
OUT2.close()
