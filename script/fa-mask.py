#!/usr/bin/env python

# Masking Given regions of the FASTA sequence

# Use modern print function from python 3.x
from __future__ import print_function

# Import modules
import argparse
from argparse import RawTextHelpFormatter
import os
import sys
import StringIO
import pandas as pd
from pandas import DataFrame
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Seq import MutableSeq
from Bio.SeqRecord import SeqRecord

# Usage
parser = argparse.ArgumentParser(
	formatter_class=RawTextHelpFormatter,
	description='Script to mask specified regions in FASTA sequence',
	usage='\n  %(prog)s --regions <FILE> FASTA > masked.fa')
parser.add_argument('fasta', metavar='FASTA', nargs=1, help='FASTA sequence to modify (required)')
parser.add_argument('--regions', metavar='FILE', nargs=1, required=True, help='Tab-separated file with 3 columns: LOCUS(Chr) START END (BED format) (required)')
parser.add_argument('--mask', metavar='N', nargs=1, default='N', help='Symbol to use for masking regions (default = "N").'
	'\nUse "--mask lc" to perform soft masking in lower case')
parser.add_argument('--out', metavar='FILE', nargs=1, help='Output file for new genome (optional - otherwise will print to stdout)')
parser.add_argument('--version', action='version', version=
	'=====================================\n'
	'%(prog)s v0.1\n'
	'Updated 31-May-2016 by Jason Kwong\n'
	'Dependencies: Python 2.x, BioPython\n'
	'=====================================')
args = parser.parse_args()

# Functions
# Log a message to stderr
def msg(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

# Log an error to stderr and quit with non-zero error code
def err(*args, **kwargs):
	msg(*args, **kwargs)
	sys.exit(1);

# Check file exists
def check_file(f):
	if os.path.isfile(f) == False:
		err('ERROR: Cannot find "{}". Check file exists in the specified directory.'.format(f))

# Check arguments
seqfile = args.fasta[0]
check_file(seqfile)
regfile = args.regions[0]
check_file(regfile)
symbol = args.mask[0]
if args.out:
	outfile = args.out[0]

# Parse masking regions
with open(regfile, 'rb') as f:
	fline = f.readline()
	if fline.startswith('#'):
		h = 0
	else:
		h = None
regions = pd.read_csv(regfile, delimiter='\t', header=h, names=['LOCUS', 'START', 'END'])
loci = regions['LOCUS'].tolist()
loci = set(loci)

# Parse sequence
seqMASK = []
fa = open(seqfile, 'rU')
for record in SeqIO.parse(fa, 'fasta'):
	msg('Reading "{}" ... '.format(record.id))
	seqlen = len(record.seq)
	if record.id in loci:
		newseq = (record.seq).tomutable()
		df = regions[regions['LOCUS'] == record.id]
		for row in df.iterrows():
			start = int(row[1][1]) - 1
			end = int(row[1][2])
			lenMASK = end - start
			if symbol == 'lc':
				newseq[start:end] = record.seq.lower()[start:end]
			else:
				newseq[start:end] = str(symbol)*lenMASK
		seqMASK.append(SeqRecord(newseq, id=record.id, name=record.name, description=record.description))
	else:
		seqMASK.append(record)

# Write masked alignment to file or print to stdout
if args.out:
	msg('Masked sequences saved to "{}" ... '.format(outfile))
	SeqIO.write(seqMASK, outfile, 'fasta')
else:
	seqFILE = StringIO.StringIO()
	SeqIO.write(seqMASK, seqFILE, 'fasta')
	output = seqFILE.getvalue().rstrip()
	print(output)

sys.exit(0)
