#!/usr/bin/env python	

import FileUtility,FastaManager,sys,os,ParseBlast,time,string,math,re

fm   = FastaManager.fasta_manager()
fu   = FileUtility.file_util()
pb   = ParseBlast.parser()
	
def parseExon(outfile):
	inp = open(outfile)
	lines=inp.readlines()
	index=0
	dict=[]
	num=0
	while (index<len(lines)):
		if lines[index].startswith("Chr"):
				split=lines[index].split()
				if split[2]=="intron":
					start=split[3]
					end=split[4]
					dict.append("-".join([split[3],split[4]]))
					num+=1
		index+=1
	if num==0:
		dict.append("---")
		return "0",";".join(dict)
	else:
		return len(dict),";".join(dict)
	

def batch_sw(pairs,fasta1,fasta2):

		(intronum,pos)=(0,0)

		program = "exonerate"
		flags   = "--model protein2genome --showvulgar no --showalignment no --maxintron 10000 --showquerygff no --showtargetgff yes --bestn 1 --ryo \"AveragePercentIdentity: %pi\\n\""

		print "Program  :",program
		print "Pair list:",pairs
		print "Fasta1   :",fasta1
		print "Fasta2   :",fasta2
		print "Flags    :",flags

		# read gene pairs
		print "Read gene pairs..."
		gpairs = fu.file_to_list(pairs,1,"\t")
		print " %i pairs" % len(gpairs)
			
		# read fasta into dict
		print "Read fasta files..."
		fd1 = fm.fasta_to_dict(fasta1)
		if fasta2 != "":
			fd2 = fm.fasta_to_dict(fasta2)
			for i in fd2:
				if i not in fd1:
					fd1[i] = fd2[i]
		
		# see if output need to be saved, if so, generate an empty file
		
		oup2 = open("%s.intr.raw" % pairs,"w")
		oup2.close()
		
		# reiterate the list and conduct sw alignment
		print "Do sw..."
		oup = open("%s.ex.out" % pairs,"w")
		c = 0
		
		for i in gpairs:
			if len(i) > 2:
				i = i[:2]
			
			if c%1e2 == 0:
				print " %i x 100" % (c/100)
			c += 1
			
			missed = 0
			if not fd1.has_key(i[0]) or not fd1.has_key(i[1]):			
				print " %s not in fasta file" % i
				oup.write("%s\t%s\n" % (i[0],i[1]))
				continue
		
			# generate temp fasta files
			oup1 = open("TMP.FA1","w")
			oup1.write(">%s\n%s\n" % (i[0],fd1[i[0]]))
			oup1.close()
			oup1 = open("TMP.FA2","w")
			oup1.write(">%s\n%s\n" % (i[1],fd1[i[1]]))
			oup1.close()
			
			# call sw and parse the output
			os.system("%s %s TMP.FA1 TMP.FA2 > TMP.OUT"%\
					   (program,flags))
			
			os.system("cat TMP.OUT >> %s.intr.raw " % (pairs))
				
			#parse exonerate results
			(intronum,pos) = parseExon("TMP.OUT")	

			#print i[0],i[1]
			# go trough the number of matching fragments

			oup.write("#%s\t%s\t%s\t%s\n" % (i[0],i[1],intronum,pos))
		
			os.system("rm TMP*")
		print "Done!"
			
pairs=sys.argv[1] # pairs  ptr.q_G50.PE_I50.PS1.pairs
fasta1=sys.argv[2] # fasta1 Ptrichocarpa_210_primary.pep
fasta2=sys.argv[3] # fasta2 ptr.q_G50.PE_I50.PS1.subj_coord.fa

batch_sw(pairs,fasta1,fasta2)

		
