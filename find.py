#!/usr/bin/env python
# -*- coding: utf-8 -*- 

'''
__author__ = 'xutengfei'
__author_email__ = 'xutengfei1@genomics.cn
Function:find sequence of id_file from genome file, need python package: biopython(pip install biopython)
'''
from Bio import SeqIO
import sys

if (len(sys.argv)==4):
	input_file,id_file,output_file=sys.argv[1],sys.argv[2],sys.argv[3]

	wanted = set(line.rstrip("\n").split(None,1)[0] for line in open(id_file))
	print ("Found %i unique identifiers in %s" % (len(wanted), id_file))
	records = (r for r in SeqIO.parse(input_file, "fasta") if r.id in wanted)
	count = SeqIO.write(records, output_file, "fasta")
	print ("Saved %i records from %s to %s" % (count, input_file, output_file))
	if count < len(wanted):
		print ("Warning %i IDs not found in %s" % (len(wanted)-count, input_file))
else:
	print("Usage: python3 fasta_file id_file out_file")