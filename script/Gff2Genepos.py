#!/usr/bin/env python
import sys,re

IN=open(sys.argv[1],'r')
OUT=open(sys.argv[2],'w')
	

for eachline in IN:
	if not eachline.startswith("#"):
		split=eachline.rstrip().split("\t")
		if split[2]=="gene":
			o=re.search("gene:(\S+?);",split[8])
			if o:
				gene=o.group(1)
			else:
				n=re.search("Name=(\S+?);",split[8])
				if n:
					gene=n.group(1)
				else:
					m=re.search("Name=(\S+)",split[8])
					if m:
						gene=m.group(1)
			OUT.write("%s\t%s\t%s\t%s\t%s\n"%(split[0],split[3],split[4],split[6],gene))
IN.close()
OUT.close()
	
