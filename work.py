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
    "-p", "--position", type=str, help="snp position file(It can only contain position.)"
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
	try:
		mydcit = collections.defaultdict(list)
		df = pd.read_table(gff,sep='\t',header=None)
		outfile = open(out,'w')
		df3 = df.iloc[:,3]  #select position and gene
		df4 = df.iloc[:,4]
		df8 = df.iloc[:,8]
		df_all = zip(df3,df4,df8) #crate a zip include df3 df4 df8 
		with open(position) as PS:
			pos = PS.readlines()
			for z in df_all:
				for a in pos:
					snp = int(a.strip())
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
