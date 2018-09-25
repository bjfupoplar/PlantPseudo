#!/usr/bin/env python
from __future__ import division
import sys,re,os,string

print '''
	Usage: python Extract_seq_previ.py  genome.fa  psedogene+gff  outfile
	       gff format:NC_001147.6     159548  160594  -	genename
	       length: bp
'''

#############################################################
signalRE = re.compile(r'AATAAA|ATTAAA|CATAAA|AATATA')
 
def checkPolya(seq):
  #==========================================
  #  determine the polya class: 1, 2 or 3
  #=========================================== [zz]

    # upcase.
    seq = seq.upper()
   
    maxCount  = 0
    maxPos = '' # if never defined, will print as null (matches original output)
    maxStr = ''

    # zz's code use <= which translate to + 1,
    # but he probably meant <, and the + 1 should be ditched
    # this is O(n^2), but could easily be made O(n)
    for i in xrange(len(seq) - 50 + 1):
        frag = seq[i:i+50]
        count = frag.count('A')
        if count > maxCount: (maxCount, maxPos, maxStr) = (count, i, frag)

    signalPos = '' # if never defined, will print as null (matches original output)
    if maxCount < 30:
        kind = 0
    else:
        mo = signalRE.search(seq[maxPos-1::-1])
        if mo:
            signalPos = mo.span()[0]
            if signalPos < 50: kind = 1
            elif signalPos <= 100: kind = 2
            else: kind = 3
        else:
            kind = 3

    return (kind, maxCount, maxPos, maxStr, signalPos)
#############################################################
def Max(i,j):
	if int(i)>=int(j):
		return int(j)
	else:
		return int(i)



def Seqin(fa):
	seq_name=[]
	seqs=[]
	each_seq=""
	for eachline in fa:
		eachline=eachline.rstrip()
		if eachline.startswith(">"):
			seq_name.append(eachline.strip(">"))
			if each_seq:
				seqs.append(each_seq)
				each_seq=""
		else:
			each_seq+=eachline
	seqs.append(each_seq)
	return seq_name,seqs

def SeqConvert(seq):
	Convert={"A":"T","C":"G","T":"A","G":"C","a":"t","t":'a',"c":'g',"g":"c","N":"N","n":"n","Y":"Y"}
	return ''.join(map(lambda x: Convert[x],seq))[::-1]
#############################################################


IN1=open(sys.argv[1],'r') # genome.fa
IN2=open(sys.argv[2],'r') # glimmer file format:Chr	159548	160594	-
kb2=int(1000) #termi N bp
OUT=open(sys.argv[3],'w')

seq_name=[]
seqs=[]
seq=""

seq_name,seqs=Seqin(IN1)
print len(seqs[0])

#for i in seq_name:
#	print ">"+i+'\n'+str(len(seq[seq_name.index(i)]))

split=[]

for eachline in IN2:
	split=eachline.rstrip().split('\t')
	try:
		if split[3]=="-":
			seq=seqs[seq_name.index(split[0])][(int(split[1])-Max(int(split[1]),kb2)):(int(split[1])-1)]
			seq=SeqConvert(seq)
		else:
			seq=seqs[seq_name.index(split[0])][int(split[2]):(int(split[2])+kb2)]
	except IndexError:
                print "pass"
	#print seq		
	(kind, maxCount, maxPos, maxStr, signalPos) = checkPolya(seq)

	OUT.write("\t".join(split+[str(n) for n in [maxCount, maxPos, maxStr, signalPos, kind]])+"\n")
		

IN1.close()
IN2.close()
OUT.close()
		
	
