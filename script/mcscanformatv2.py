#!/us/bin/env python
import sys,re

in1=open(sys.argv[1],'r')#sample.pep
in2=open(sys.argv[2],'r')#gene.pos
OUT=open(sys.argv[3],'w')

#Chr1    3631    5899    +       AT1G01010
#sp#Chr01        Potri.001G003900        230619  245043

glst=[]
for eachline in in1:
	m=re.match(">(\S+)",eachline)
	if m:
		glst.append(m.group(1))


for eachline in in2:
	split=eachline.rstrip().split("\t")
	if split[4] in glst:
		OUT.write("sp#%s\t%s\t%s\t%s\n"%(split[0],split[4],split[1],split[2]))

in1.close()
in2.close()
OUT.close()
