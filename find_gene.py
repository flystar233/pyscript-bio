#!/usr/bin/env python
# coding=utf-8

import os
import pandas as pd
import click
import collections

@click.command()
@click.option(
    "-g", "--gff", type=str, help="gff file (It can only contain one chromosome.)"
    )
@click.option(
    "-p", "--position", type=str, help="chromosome name and snp position file(chr1  123456789)"
    )
@click.option(
    "-w", "--width", default=1000000, type=int, help="Total length of upstream and downstream of SNP locus (default 1M)"
)
@click.option(
    "-o",
    "--out",
    default="out.txt",
    type=str,
    help="Output file (default 'out.txt')")

def command_line_runner(gff,position,width,out):
	"""
	According to the results of GWAS, the genes of upstream and downstream 1M of SNP locus were selected.
	"""
	_VERSION = "1.1.1"
	try:
    	print("--------------------------------------------\nLooking for genes...\nThe gene and iterative position will be saved in {}".format(out))
		mydcit = collections.defaultdict(list)
		df = pd.read_table(gff,sep='\t',header=None)
		pos = pd.read_table(position,sep='\t',header=None)
		outfile = open(out,'w')
		df3 = df.iloc[:,3]  #select position and gene
		df4 = df.iloc[:,4]
		df8 = df.iloc[:,8]
		df_all = zip(df3,df4,df8) #crate a zip include df3 df4 df8
		posnow = pos.iloc[:,1]
		for z in df_all:
			for a in posnow:
				snp = int(a)
				snpdown = snp - width/2 #set downstream
				for i in range(0,width+1,1000):
					snpnow = snpdown +i
					if z[0] <= snpnow < z[1]:
						mydcit[z[2]].append(snpnow)
		outfile.write("gene\tposition\n")
		for key in mydcit.keys():
			outfile.write("{}\t{}\n".format(key,mydcit[key]))
		number = len(mydcit.keys())
		print("There are {} gene in {}".format(number,out))
	except:
		print("Please input your option, or use --help")
	
if __name__ == "__main__":
	command_line_runner()
